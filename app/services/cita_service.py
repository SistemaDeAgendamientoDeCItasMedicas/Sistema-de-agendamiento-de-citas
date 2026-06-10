from app.domain.cita_model import Cita, CitaCreate
from app.repositories import cita_repository
from app.repositories import paciente_repository
from app.repositories import medico_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class PacienteNoEncontradoError(Exception):
    """El paciente no existe en el sistema."""
    pass


class MedicoNoEncontradoError(Exception):
    """El médico no existe en el sistema."""
    pass


class PacienteInactivoError(Exception):
    """El paciente existe pero está inactivo."""
    pass


class MedicoInactivoError(Exception):
    """El médico existe pero está inactivo."""
    pass


class ConflictoHorarioMedicoError(Exception):
    """El médico ya tiene una cita en ese horario."""
    pass


class ConflictoHorarioPacienteError(Exception):
    """El paciente ya tiene una cita en ese horario."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al procesar el agendamiento."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def agendar_cita(datos: CitaCreate) -> Cita:
    """
    Agenda una cita médica en el sistema.

    Reglas de negocio:
    1. El paciente debe existir y estar activo.
    2. El médico debe existir y estar activo.
    3. El médico no debe tener otra cita en ese horario (±30 min).
    4. El paciente no debe tener otra cita en ese horario (±30 min).
    5. La fecha y hora ya fueron validadas por Pydantic (no pasada, horario laboral).

    Lanza:
    - PacienteNoEncontradoError      → HTTP 404
    - MedicoNoEncontradoError        → HTTP 404
    - PacienteInactivoError          → HTTP 403
    - MedicoInactivoError            → HTTP 403
    - ConflictoHorarioMedicoError    → HTTP 409
    - ConflictoHorarioPacienteError  → HTTP 409
    - ErrorInternoError              → HTTP 500
    """
    # Regla 1: paciente debe existir
    paciente = paciente_repository.obtener_por_id(datos.patient_id)
    if not paciente:
        raise PacienteNoEncontradoError(
            f"Patient with ID {datos.patient_id} not found"
        )

    # Regla 1b: paciente debe estar activo
    if paciente.estado.value != "ACTIVO":
        raise PacienteInactivoError(
            f"Patient with ID {datos.patient_id} is not active"
        )

    # Regla 2: médico debe existir
    medico = medico_repository.obtener_por_id(datos.doctor_id)
    if not medico:
        raise MedicoNoEncontradoError(
            f"Doctor with ID {datos.doctor_id} not found"
        )

    # Regla 2b: médico debe estar activo
    if medico.estado.value != "ACTIVO":
        raise MedicoInactivoError(
            f"Doctor with ID {datos.doctor_id} is not active"
        )

    # Regla 3: disponibilidad del médico
    if cita_repository.existe_conflicto_medico(datos.doctor_id, datos.date, datos.time):
        raise ConflictoHorarioMedicoError(
            "Doctor is not available at the requested time"
        )

    # Regla 4: disponibilidad del paciente
    if cita_repository.existe_conflicto_paciente(datos.patient_id, datos.date, datos.time):
        raise ConflictoHorarioPacienteError(
            "Patient already has an appointment at the requested time"
        )

    try:
        cita = cita_repository.guardar_cita(datos)
        return cita
    except Exception as e:
        raise ErrorInternoError("Error scheduling appointment") from e