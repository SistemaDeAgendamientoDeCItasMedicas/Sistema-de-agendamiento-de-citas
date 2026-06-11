from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from app.domain.cita_model import CitaCreate, CitaResponse, CitaData, EstadoCita
from app.domain.reprogramar_model import ReprogramarCitaRequest
from app.services import cita_service
from app.services import consultar_cita_service
from app.services import cancelar_cita_service
from app.services import reprogramar_cita_service
from app.services import listar_citas_service
from app.services import eliminar_cita_service
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
    CitaNoEncontradaError as CancelCitaNoEncontrada,
    CitaYaCanceladaError,
    CitaCompletadaError as CancelCitaCompletada,
    TiempoCancelacionExcedidoError,
    ErrorInternoError as CancelErrorInterno,
)
from app.services.reprogramar_cita_service import (
    CitaNoEncontradaError as ReprogramarCitaNoEncontrada,
    CitaNoReprogramableError,
    ConflictoHorarioMedicoError as ReprogramarConflictoMedico,
    ConflictoHorarioPacienteError as ReprogramarConflictoPaciente,
    ErrorInternoError as ReprogramarErrorInterno,
)
from app.services.listar_citas_service import (
    TamanoPaginaExcedidoError,
    ErrorInternoError as ListarErrorInterno,
)
from app.services.eliminar_cita_service import (
    CitaNoEncontradaError as EliminarCitaNoEncontrada,
    CitaCompletadaError as EliminarCitaCompletada,
    CitaYaEliminadaError,
    ErrorInternoError as EliminarErrorInterno,
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e), "success": False})
    except (PacienteInactivoError, MedicoInactivoError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": str(e), "success": False})
    except (ConflictoHorarioMedicoError, ConflictoHorarioPacienteError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": str(e), "success": False})
    except ErrorInternoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "success": False})


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
    Consulta citas con filtros opcionales y paginación.

    **Requiere autenticación:** Bearer Token JWT.

    **Filtros opcionales:** date, patient_id, doctor_id, status

    **Paginación:** page (default: 1), size (default: 10, máximo: 100)
    """
    date_filter = None
    if date:
        try:
            from datetime import date as DateType
            date_filter = DateType.fromisoformat(date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Invalid date format. Must be YYYY-MM-DD", "success": False},
            )

    try:
        citas, total = consultar_cita_service.consultar_citas(
            date_filter=date_filter, patient_id=patient_id,
            doctor_id=doctor_id, status=status_filter, page=page, size=size,
        )
        total_pages = math.ceil(total / size) if total > 0 else 0

        if not citas:
            return {"message": "No appointments found", "data": [],
                    "pagination": {"page": page, "size": size, "total_records": 0, "total_pages": 0}, "success": False}

        return {
            "message": "Appointments retrieved successfully",
            "data": [{"appointment_id": c.id, "patient_id": c.patient_id, "doctor_id": c.doctor_id,
                      "date": str(c.date), "time": c.time, "reason": c.reason, "status": c.status} for c in citas],
            "pagination": {"page": page, "size": size, "total_records": total, "total_pages": total_pages},
            "success": True,
        }
    except ConsultaErrorInterno as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "success": False})


# ─── HU-07: PATCH cancel ─────────────────────────────────────────────────────

@router.patch(
    "/{appointment_id}/cancel",
    status_code=status.HTTP_200_OK,
    summary="[HU-07] Cancelar cita médica",
    tags=["[HU-07] Cancelar Cita Médica"],
    responses={
        200: {"description": "Appointment cancelled successfully"},
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

    **Reglas:** estado SCHEDULED o RESCHEDULED, mínimo 1 hora de anticipación.

    **Estado resultante:** `CANCELLED`
    """
    try:
        cita = cancelar_cita_service.cancelar_cita(appointment_id)
        return {"message": "Appointment cancelled successfully",
                "data": {"appointment_id": cita.id, "status": cita.status}, "success": True}
    except CancelCitaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e), "success": False})
    except (CitaYaCanceladaError, CancelCitaCompletada) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": str(e), "success": False})
    except TiempoCancelacionExcedidoError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e), "success": False})
    except CancelErrorInterno as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "success": False})


# ─── HU-08: PATCH reschedule ─────────────────────────────────────────────────

@router.patch(
    "/{appointment_id}/reschedule",
    status_code=status.HTTP_200_OK,
    summary="[HU-08] Reprogramar cita médica",
    tags=["[HU-08] Reprogramar Cita Médica"],
    responses={
        200: {"description": "Appointment rescheduled successfully"},
        400: {"description": "Fecha pasada u hora fuera del horario laboral"},
        401: {"description": "Token inválido o no enviado"},
        404: {"description": "Cita no encontrada"},
        409: {"description": "Cita no reprogramable o médico no disponible"},
        500: {"description": "Error interno del servidor"},
    },
)
def reprogramar_cita(
    appointment_id: int,
    datos: ReprogramarCitaRequest,
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Reprograma una cita médica existente.

    **Requiere autenticación:** Bearer Token JWT.

    **Reglas:** estado SCHEDULED o RESCHEDULED, nueva fecha futura, médico disponible.

    **Estado resultante:** `RESCHEDULED`
    """
    try:
        cita = reprogramar_cita_service.reprogramar_cita(appointment_id, datos)
        return {
            "message": "Appointment rescheduled successfully",
            "data": {"appointment_id": cita.id, "patient_id": cita.patient_id,
                     "doctor_id": cita.doctor_id, "date": str(cita.date),
                     "time": cita.time, "reason": cita.reason, "status": cita.status},
            "success": True,
        }
    except ReprogramarCitaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e), "success": False})
    except CitaNoReprogramableError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": str(e), "success": False})
    except (ReprogramarConflictoMedico, ReprogramarConflictoPaciente) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": str(e), "success": False})
    except ReprogramarErrorInterno as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "success": False})


# ─── HU-09: GET list ─────────────────────────────────────────────────────────

@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    summary="[HU-09] Listar citas médicas",
    tags=["[HU-09] Listar Citas Médicas"],
    responses={
        200: {"description": "Appointments listed successfully"},
        400: {"description": "Parámetros inválidos o tamaño excedido"},
        401: {"description": "Token inválido o no enviado"},
        500: {"description": "Error interno del servidor"},
    },
)
def listar_citas(
    page: int = Query(1, ge=1, description="Número de página (mínimo: 1)"),
    size: int = Query(10, ge=1, description="Registros por página (máximo: 50)"),
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Lista todas las citas médicas con paginación obligatoria.

    **Requiere autenticación:** Bearer Token JWT.

    **Paginación:** page (default: 1), size (default: 10, máximo: 50)

    **Ordenamiento:** fecha y hora ascendente.
    """
    try:
        citas, total = listar_citas_service.listar_citas(page=page, size=size)
        total_pages = math.ceil(total / size) if total > 0 else 0

        if not citas:
            return {"message": "No appointments registered", "data": [],
                    "pagination": {"page": page, "size": size, "total_records": 0, "total_pages": 0}, "success": False}

        return {
            "message": "Appointments listed successfully",
            "data": [{"appointment_id": c.id, "patient_id": c.patient_id, "doctor_id": c.doctor_id,
                      "date": str(c.date), "time": c.time, "reason": c.reason, "status": c.status} for c in citas],
            "pagination": {"page": page, "size": size, "total_records": total, "total_pages": total_pages},
            "success": True,
        }
    except TamanoPaginaExcedidoError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e), "success": False})
    except ListarErrorInterno as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "success": False})


# ─── HU-10: DELETE ───────────────────────────────────────────────────────────

@router.delete(
    "/{appointment_id}",
    status_code=status.HTTP_200_OK,
    summary="[HU-10] Eliminar cita médica",
    tags=["[HU-10] Eliminar Cita Médica"],
    responses={
        200: {
            "description": "Appointment deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Appointment deleted successfully",
                        "data": {"appointment_id": 1, "status": "DELETED"},
                        "success": True,
                    }
                }
            },
        },
        401: {"description": "Token inválido o no enviado"},
        404: {
            "description": "Cita no encontrada",
            "content": {
                "application/json": {
                    "example": {"message": "Appointment not found", "success": False}
                }
            },
        },
        409: {
            "description": "Cita completada o ya eliminada",
            "content": {
                "application/json": {
                    "example": {"message": "Cannot delete a completed appointment", "success": False}
                }
            },
        },
        500: {"description": "Error interno del servidor"},
    },
)
def eliminar_cita(
    appointment_id: int,
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Elimina lógicamente una cita médica (soft delete).

    **Requiere autenticación:** Bearer Token JWT.

    **Reglas de eliminación:**
    - La cita debe existir en el sistema
    - La cita no debe estar en estado `COMPLETED`
    - La cita no debe estar ya en estado `DELETED`
    - El registro se conserva para auditoría

    **Estado resultante:** `DELETED`
    """
    try:
        cita = eliminar_cita_service.eliminar_cita(appointment_id)
        return {
            "message": "Appointment deleted successfully",
            "data": {
                "appointment_id": cita.id,
                "status": cita.status,
            },
            "success": True,
        }
    except EliminarCitaNoEncontrada as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e), "success": False},
        )
    except (EliminarCitaCompletada, CitaYaEliminadaError) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": str(e), "success": False},
        )
    except EliminarErrorInterno as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": str(e), "success": False},
        )


# ─── Endpoints auxiliares para pruebas ───────────────────────────────────────

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

    **Uso:** endpoint auxiliar para probar Caso 3 de HU-10 y Caso 4 de HU-07.
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
    return {"message": f"Appointment {appointment_id} marked as completed", "success": True}