from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from datetime import date
from app.domain.cita_model import CitaCreate, CitaResponse, CitaData, EstadoCita
from app.services import cita_service
from app.services import consultar_cita_service
from app.services.cita_service import (
    PacienteNoEncontradoError,
    MedicoNoEncontradoError,
    PacienteInactivoError,
    MedicoInactivoError,
    ConflictoHorarioMedicoError,
    ConflictoHorarioPacienteError,
    ErrorInternoError,
)
from app.services.consultar_cita_service import ErrorInternoError as ConsultaErrorInterno
from app.core.dependencies import get_current_user
import math

router = APIRouter(
    prefix="/api/v1/citas",
    tags=["[HU-05] Agendar Cita Médica", "[HU-06] Consultar Citas Médicas"],
)


# ─── HU-05: POST ─────────────────────────────────────────────────────────────

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CitaResponse,
    summary="[HU-05] Agendar cita médica",
    responses={
        201: {"description": "Appointment scheduled successfully"},
        400: {"description": "Fecha pasada u hora fuera del horario laboral"},
        401: {"description": "Token inválido o no enviado"},
        403: {"description": "Paciente o médico inactivo"},
        404: {"description": "Paciente o médico no encontrado"},
        409: {"description": "Conflicto de horario"},
        500: {"description": "Error interno del servidor"},
    },
)
def agendar_cita(
    datos: CitaCreate,
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Agenda una nueva cita médica en el sistema.

    **Requiere autenticación:** Bearer Token JWT.

    **Validaciones:**
    - `patient_id`: debe existir y estar activo
    - `doctor_id`: debe existir y estar activo
    - `date`: formato YYYY-MM-DD, no puede ser fecha pasada
    - `time`: formato HH:MM, entre 08:00 y 18:00
    - `reason`: mínimo 5 caracteres

    **Estado inicial:** `SCHEDULED`
    """
    try:
        cita = cita_service.agendar_cita(datos)
        return CitaResponse(
            message="Appointment scheduled successfully",
            data=CitaData(
                appointment_id=cita.id,
                patient_id=cita.patient_id,
                doctor_id=cita.doctor_id,
                date=str(cita.date),
                time=cita.time,
                reason=cita.reason,
                status=cita.status,
            ),
            success=True,
        )

    except (PacienteNoEncontradoError, MedicoNoEncontradoError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e), "success": False},
        )
    except (PacienteInactivoError, MedicoInactivoError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": str(e), "success": False},
        )
    except (ConflictoHorarioMedicoError, ConflictoHorarioPacienteError) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": str(e), "success": False},
        )
    except ErrorInternoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": str(e), "success": False},
        )


# ─── HU-06: GET ──────────────────────────────────────────────────────────────

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="[HU-06] Consultar citas médicas",
    responses={
        200: {
            "description": "Appointments retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Appointments retrieved successfully",
                        "data": [
                            {
                                "appointment_id": 1,
                                "patient_id": 1,
                                "doctor_id": 2,
                                "date": "2026-05-10",
                                "time": "10:00",
                                "reason": "Consulta general",
                                "status": "SCHEDULED",
                            }
                        ],
                        "pagination": {
                            "page": 1,
                            "size": 10,
                            "total_records": 1,
                            "total_pages": 1,
                        },
                        "success": True,
                    }
                }
            },
        },
        400: {
            "description": "Formato de fecha inválido",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid date format. Must be YYYY-MM-DD",
                        "success": False,
                    }
                }
            },
        },
        401: {
            "description": "Token inválido o no enviado",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid or missing token",
                        "success": False,
                    }
                }
            },
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Error retrieving appointments",
                        "success": False,
                    }
                }
            },
        },
    },
)
def consultar_citas(
    date: Optional[str] = Query(None, description="Filtrar por fecha (YYYY-MM-DD)"),
    patient_id: Optional[int] = Query(None, description="Filtrar por ID de paciente"),
    doctor_id: Optional[int] = Query(None, description="Filtrar por ID de médico"),
    status_filter: Optional[EstadoCita] = Query(None, alias="status", description="Filtrar por estado"),
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Registros por página"),
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Consulta las citas médicas registradas con filtros opcionales y paginación.

    **Requiere autenticación:** Bearer Token JWT.

    **Filtros opcionales:**
    - `date`: fecha en formato YYYY-MM-DD
    - `patient_id`: ID del paciente
    - `doctor_id`: ID del médico
    - `status`: SCHEDULED | CANCELLED | RESCHEDULED | COMPLETED

    **Paginación:**
    - `page`: número de página (default: 1)
    - `size`: registros por página (default: 10, máximo: 100)
    """
    # Validar y parsear fecha si se envió
    date_filter = None
    if date:
        try:
            from datetime import date as DateType
            date_filter = DateType.fromisoformat(date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid date format. Must be YYYY-MM-DD",
                    "success": False,
                },
            )

    try:
        citas, total = consultar_cita_service.consultar_citas(
            date_filter=date_filter,
            patient_id=patient_id,
            doctor_id=doctor_id,
            status=status_filter,
            page=page,
            size=size,
        )

        total_pages = math.ceil(total / size) if total > 0 else 0

        if not citas:
            return {
                "message": "No appointments found",
                "data": [],
                "pagination": {
                    "page": page,
                    "size": size,
                    "total_records": 0,
                    "total_pages": 0,
                },
                "success": False,
            }

        return {
            "message": "Appointments retrieved successfully",
            "data": [
                {
                    "appointment_id": c.id,
                    "patient_id": c.patient_id,
                    "doctor_id": c.doctor_id,
                    "date": str(c.date),
                    "time": c.time,
                    "reason": c.reason,
                    "status": c.status,
                }
                for c in citas
            ],
            "pagination": {
                "page": page,
                "size": size,
                "total_records": total,
                "total_pages": total_pages,
            },
            "success": True,
        }

    except ConsultaErrorInterno as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": str(e), "success": False},
        )