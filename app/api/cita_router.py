from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from datetime import date
from app.domain.cita_model import CitaCreate, CitaResponse, CitaData, EstadoCita
from app.services import cita_service
from app.services import consultar_cita_service
from app.services import cancelar_cita_service
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
from app.services.cancelar_cita_service import (
    CitaNoEncontradaError,
    CitaYaCanceladaError,
    CitaCompletadaError,
    TiempoCancelacionExcedidoError,
    ErrorInternoError as CancelErrorInterno,
)
from app.core.dependencies import get_current_user
import math

router = APIRouter(prefix="/api/v1/citas")


# ─── HU-05: POST ─────────────────────────────────────────────────────────────

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CitaResponse,
    summary="[HU-05] Agendar cita médica",
    tags=["[HU-05] Agendar Cita Médica"],
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
    tags=["[HU-06] Consultar Citas Médicas"],
    responses={
        200: {"description": "Appointments retrieved successfully"},
        400: {"description": "Formato de fecha inválido"},
        401: {"description": "Token inválido o no enviado"},
        500: {"description": "Error interno del servidor"},
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


# ─── HU-07: PATCH cancel ─────────────────────────────────────────────────────

@router.patch(
    "/{appointment_id}/cancel",
    status_code=status.HTTP_200_OK,
    summary="[HU-07] Cancelar cita médica",
    tags=["[HU-07] Cancelar Cita Médica"],
    responses={
        200: {
            "description": "Appointment cancelled successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Appointment cancelled successfully",
                        "data": {"appointment_id": 1, "status": "CANCELLED"},
                        "success": True,
                    }
                }
            },
        },
        400: {"description": "Cancelación fuera del tiempo permitido"},
        401: {"description": "Token inválido o no enviado"},
        404: {"description": "Cita no encontrada"},
        409: {"description": "Cita ya cancelada o completada"},
        500: {"description": "Error interno del servidor"},
    },
)
def cancelar_cita(
    appointment_id: int,
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Cancela una cita médica existente.

    **Requiere autenticación:** Bearer Token JWT.

    **Reglas de cancelación:**
    - La cita debe existir en el sistema
    - La cita debe estar en estado `SCHEDULED` o `RESCHEDULED`
    - La cancelación debe realizarse con al menos 1 hora de anticipación

    **Estado resultante:** `CANCELLED`
    """
    try:
        cita = cancelar_cita_service.cancelar_cita(appointment_id)
        return {
            "message": "Appointment cancelled successfully",
            "data": {
                "appointment_id": cita.id,
                "status": cita.status,
            },
            "success": True,
        }
    except CitaNoEncontradaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e), "success": False},
        )
    except (CitaYaCanceladaError, CitaCompletadaError) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": str(e), "success": False},
        )
    except TiempoCancelacionExcedidoError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "success": False},
        )
    except CancelErrorInterno as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": str(e), "success": False},
        )


# ─── Endpoint auxiliar para pruebas ──────────────────────────────────────────

@router.patch(
    "/{appointment_id}/complete",
    summary="Completar cita (solo pruebas)",
    tags=["[HU-07] Cancelar Cita Médica"],
)
def completar_cita(
    appointment_id: int,
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Marca una cita como completada.

    **Uso:** endpoint auxiliar para probar el Caso 4 de HU-07
    (cancelar cita completada → 409 Conflict).
    """
    from app.repositories import cita_repository
    from app.domain.cita_model import EstadoCita

    cita = cita_repository.obtener_por_id(appointment_id)

    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Appointment not found", "success": False},
        )

    cita_repository.actualizar_estado(appointment_id, EstadoCita.COMPLETED)

    return {
        "message": f"Appointment {appointment_id} marked as completed",
        "success": True,
    }