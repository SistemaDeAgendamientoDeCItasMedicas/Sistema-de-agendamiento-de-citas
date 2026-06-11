from app.domain.cita_model import Cita, EstadoCita
from app.repositories import cita_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class CitaNoEncontradaError(Exception):
    """La cita no existe en el sistema."""
    pass


class CitaCompletadaError(Exception):
    """No se puede eliminar una cita completada."""
    pass


class CitaYaEliminadaError(Exception):
    """La cita ya tiene estado DELETED."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al eliminar la cita."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def eliminar_cita(appointment_id: int) -> Cita:
    """
    Elimina lógicamente una cita médica (soft delete).

    Reglas de negocio:
    1. La cita debe existir en el sistema.
    2. La cita no debe estar en estado COMPLETED.
    3. La cita no debe estar ya en estado DELETED.
    4. Se aplica soft delete — el registro permanece para auditoría.
    5. El estado se actualiza a DELETED.

    Lanza:
    - CitaNoEncontradaError  → HTTP 404
    - CitaCompletadaError    → HTTP 409
    - CitaYaEliminadaError   → HTTP 409
    - ErrorInternoError      → HTTP 500
    """
    # Regla 1: la cita debe existir
    cita = cita_repository.obtener_por_id(appointment_id)
    if not cita:
        raise CitaNoEncontradaError("Appointment not found")

    # Regla 2: no debe estar completada
    if cita.status == EstadoCita.COMPLETED:
        raise CitaCompletadaError("Cannot delete a completed appointment")

    # Regla 3: no debe estar ya eliminada
    if cita.status == EstadoCita.DELETED:
        raise CitaYaEliminadaError("Appointment is already deleted")

    try:
        # Regla 4 y 5: soft delete → estado DELETED
        cita_eliminada = cita_repository.actualizar_estado(
            appointment_id, EstadoCita.DELETED
        )
        return cita_eliminada
    except Exception as e:
        raise ErrorInternoError("Error deleting appointment") from e