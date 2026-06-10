from fastapi import APIRouter, HTTPException, status, Depends
from app.domain.cita_model import CitaCreate, CitaResponse, CitaData
from app.services import cita_service
from app.services.cita_service import (
    PacienteNoEncontradoError,
    MedicoNoEncontradoError,
    PacienteInactivoError,
    MedicoInactivoError,
    ConflictoHorarioMedicoError,
    ConflictoHorarioPacienteError,
    ErrorInternoError,
)
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/citas",
    tags=["[HU-05] Agendar Cita Médica"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CitaResponse,
    summary="[HU-05] Agendar cita médica",
    responses={
        201: {
            "description": "Appointment scheduled successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Appointment scheduled successfully",
                        "data": {
                            "appointment_id": 1,
                            "patient_id": 1,
                            "doctor_id": 2,
                            "date": "2026-05-10",
                            "time": "10:00",
                            "reason": "Consulta general",
                            "status": "SCHEDULED",
                        },
                        "success": True,
                    }
                }
            },
        },
        400: {
            "description": "Fecha pasada u hora fuera del horario laboral",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Time must be between 08:00 and 18:00",
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
        403: {
            "description": "Paciente o médico inactivo",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Doctor is not active",
                        "success": False,
                    }
                }
            },
        },
        404: {
            "description": "Paciente o médico no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Patient not found",
                        "success": False,
                    }
                }
            },
        },
        409: {
            "description": "Conflicto de horario",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Doctor is not available at the requested time",
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
                        "message": "Error scheduling appointment",
                        "success": False,
                    }
                }
            },
        },
    },
)
def agendar_cita(
    datos: CitaCreate,
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Agenda una nueva cita médica en el sistema.

    **Requiere autenticación:** Bearer Token JWT (obtenido en HU-02 login).

    **Validaciones aplicadas:**
    - `patient_id`: debe existir y estar activo
    - `doctor_id`: debe existir y estar activo
    - `date`: formato YYYY-MM-DD, no puede ser fecha pasada
    - `time`: formato HH:MM, entre 08:00 y 18:00
    - `reason`: mínimo 5 caracteres

    **Reglas de negocio:**
    - El médico no puede tener otra cita en el mismo horario (±30 minutos)
    - El paciente no puede tener otra cita en el mismo horario (±30 minutos)

    **Estado inicial asignado:** `SCHEDULED`
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