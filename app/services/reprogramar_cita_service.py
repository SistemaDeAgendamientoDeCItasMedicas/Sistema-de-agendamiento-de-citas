from datetime import date
from app.domain.cita_model import Cita, EstadoCita
from app.domain.reprogramar_model import ReprogramarCitaRequest
from app.repositories import cita_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class CitaNoEncontradaError(Exception):
    """La cita no existe en el sistema."""
    pass


class CitaNoReprogramableError(Exception):
    """La cita está cancelada o completada."""
    pass


class ConflictoHorarioMedicoError(Exception):
    """El médico ya tiene una cita en ese horario."""
    pass


class ConflictoHorarioPacienteError(Exception):
    """El paciente ya tiene una cita en ese horario."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al reprogramar la cita."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def reprogramar_cita(
    appointment_id: int,
    datos: ReprogramarCitaRequest,
) -> Cita:
    """
    Reprograma una cita médica existente.

    Reglas de negocio:
    1. La cita debe existir en el sistema.
    2. La cita no debe estar en estado CANCELLED ni COMPLETED.
    3. La nueva fecha y hora ya fueron validadas por Pydantic.
    4. El médico debe estar disponible en el nuevo horario.
    5. El paciente debe estar disponible en el nuevo horario.
    6. El estado se actualiza a RESCHEDULED.

    Lanza:
    - CitaNoEncontradaError        → HTTP 404
    - CitaNoReprogramableError     → HTTP 409
    - ConflictoHorarioMedicoError  → HTTP 409
    - ConflictoHorarioPacienteError → HTTP 409
    - ErrorInternoError            → HTTP 500
    """
    # Regla 1: la cita debe existir
    cita = cita_repository.obtener_por_id(appointment_id)
    if not cita:
        raise CitaNoEncontradaError("Appointment not found")

    # Regla 2: no debe estar cancelada ni completada
    if cita.status in [EstadoCita.CANCELLED, EstadoCita.COMPLETED]:
        raise CitaNoReprogramableError(
            "Cannot reschedule a cancelled or completed appointment"
        )

    # Regla 4: disponibilidad del médico (excluyendo la cita actual)
    if cita_repository.existe_conflicto_medico(
        cita.doctor_id, datos.date, datos.time,
        excluir_cita_id=appointment_id
    ):
        raise ConflictoHorarioMedicoError(
            "Doctor is not available at the requested time"
        )

    # Regla 5: disponibilidad del paciente (excluyendo la cita actual)
    if cita_repository.existe_conflicto_paciente(
        cita.patient_id, datos.date, datos.time,
        excluir_cita_id=appointment_id
    ):
        raise ConflictoHorarioPacienteError(
            "Patient already has an appointment at the requested time"
        )

    try:
        cita_actualizada = cita_repository.reprogramar_cita(
            appointment_id, datos.date, datos.time
        )
        return cita_actualizada
    except Exception as e:
        raise ErrorInternoError("Error rescheduling appointment") from e