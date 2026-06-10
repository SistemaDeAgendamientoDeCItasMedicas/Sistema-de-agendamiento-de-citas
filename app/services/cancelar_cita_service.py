from datetime import datetime, timezone, timedelta
from app.domain.cita_model import Cita, EstadoCita
from app.repositories import cita_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class CitaNoEncontradaError(Exception):
    """La cita no existe en el sistema."""
    pass


class CitaYaCanceladaError(Exception):
    """La cita ya tiene estado CANCELLED."""
    pass


class CitaCompletadaError(Exception):
    """No se puede cancelar una cita completada."""
    pass


class TiempoCancelacionExcedidoError(Exception):
    """La cancelación debe hacerse con al menos 1 hora de anticipación."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al cancelar la cita."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def cancelar_cita(appointment_id: int) -> Cita:
    """
    Cancela una cita médica existente.

    Reglas de negocio:
    1. La cita debe existir en el sistema.
    2. La cita no debe estar en estado CANCELLED.
    3. La cita no debe estar en estado COMPLETED.
    4. La cancelación debe realizarse con al menos 1 hora de anticipación.
    5. El estado se actualiza a CANCELLED.

    Lanza:
    - CitaNoEncontradaError           → HTTP 404
    - CitaYaCanceladaError            → HTTP 409
    - CitaCompletadaError             → HTTP 409
    - TiempoCancelacionExcedidoError  → HTTP 400
    - ErrorInternoError               → HTTP 500
    """
    # Regla 1: la cita debe existir
    cita = cita_repository.obtener_por_id(appointment_id)
    if not cita:
        raise CitaNoEncontradaError("Appointment not found")

    # Regla 2: no debe estar cancelada
    if cita.status == EstadoCita.CANCELLED:
        raise CitaYaCanceladaError("Appointment is already cancelled")

    # Regla 3: no debe estar completada
    if cita.status == EstadoCita.COMPLETED:
        raise CitaCompletadaError("Cannot cancel a completed appointment")

    # Regla 4: anticipación mínima de 1 hora
    ahora = datetime.now(timezone.utc)
    fecha_hora_cita = datetime.combine(cita.date, datetime.strptime(cita.time, "%H:%M").time())
    fecha_hora_cita = fecha_hora_cita.replace(tzinfo=timezone.utc)

    if fecha_hora_cita - ahora < timedelta(hours=1):
        raise TiempoCancelacionExcedidoError(
            "Cancellation deadline exceeded. Must cancel at least 1 hour in advance"
        )

    try:
        # Regla 5: actualizar estado a CANCELLED
        cita_actualizada = cita_repository.actualizar_estado(
            appointment_id, EstadoCita.CANCELLED
        )
        return cita_actualizada
    except Exception as e:
        raise ErrorInternoError("Error cancelling appointment") from e