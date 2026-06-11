from typing import Optional
from datetime import datetime, timezone, date, timedelta
from app.domain.cita_model import Cita, CitaCreate, EstadoCita


# ─── Almacenamiento en memoria ───────────────────────────────────────────────
_citas: dict[int, Cita] = {}
_siguiente_id: int = 1


def guardar_cita(datos: CitaCreate) -> Cita:
    """Persiste una nueva cita y retorna la entidad creada."""
    global _siguiente_id

    nueva = Cita(
        id=_siguiente_id,
        patient_id=datos.patient_id,
        doctor_id=datos.doctor_id,
        date=datos.date,
        time=datos.time,
        reason=datos.reason,
        status=EstadoCita.SCHEDULED,
        created_at=datetime.now(timezone.utc),
    )

    _citas[_siguiente_id] = nueva
    _siguiente_id += 1
    return nueva


def obtener_por_id(cita_id: int) -> Optional[Cita]:
    """Busca una cita por su ID."""
    return _citas.get(cita_id)


def listar_con_filtros(
    date_filter: Optional[date] = None,
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    status: Optional[EstadoCita] = None,
    page: int = 1,
    size: int = 10,
) -> tuple[list[Cita], int]:
    """Retorna citas filtradas y paginadas."""
    resultados = list(_citas.values())

    if date_filter:
        resultados = [c for c in resultados if c.date == date_filter]
    if patient_id:
        resultados = [c for c in resultados if c.patient_id == patient_id]
    if doctor_id:
        resultados = [c for c in resultados if c.doctor_id == doctor_id]
    if status:
        resultados = [c for c in resultados if c.status == status]

    resultados.sort(key=lambda c: (c.date, c.time))
    total = len(resultados)

    inicio = (page - 1) * size
    fin = inicio + size
    return resultados[inicio:fin], total


def listar_todas() -> list[Cita]:
    """Retorna todas las citas registradas."""
    return list(_citas.values())


def listar_por_medico(doctor_id: int) -> list[Cita]:
    """Retorna todas las citas de un médico específico."""
    return [c for c in _citas.values() if c.doctor_id == doctor_id]


def listar_por_paciente(patient_id: int) -> list[Cita]:
    """Retorna todas las citas de un paciente específico."""
    return [c for c in _citas.values() if c.patient_id == patient_id]


def existe_conflicto_medico(
    doctor_id: int,
    fecha: date,
    hora: str,
    excluir_cita_id: Optional[int] = None,
) -> bool:
    """Verifica si el médico ya tiene una cita en ese horario (±30 minutos)."""
    hora_solicitada = datetime.strptime(hora, "%H:%M")
    margen = timedelta(minutes=30)

    for cita in _citas.values():
        if excluir_cita_id and cita.id == excluir_cita_id:
            continue
        if (
            cita.doctor_id == doctor_id
            and cita.date == fecha
            and cita.status not in [EstadoCita.CANCELLED]
        ):
            hora_cita = datetime.strptime(cita.time, "%H:%M")
            if abs(hora_solicitada - hora_cita) < margen:
                return True
    return False


def existe_conflicto_paciente(
    patient_id: int,
    fecha: date,
    hora: str,
    excluir_cita_id: Optional[int] = None,
) -> bool:
    """Verifica si el paciente ya tiene una cita en ese horario (±30 minutos)."""
    hora_solicitada = datetime.strptime(hora, "%H:%M")
    margen = timedelta(minutes=30)

    for cita in _citas.values():
        if excluir_cita_id and cita.id == excluir_cita_id:
            continue
        if (
            cita.patient_id == patient_id
            and cita.date == fecha
            and cita.status not in [EstadoCita.CANCELLED]
        ):
            hora_cita = datetime.strptime(cita.time, "%H:%M")
            if abs(hora_solicitada - hora_cita) < margen:
                return True
    return False


def actualizar_estado(cita_id: int, nuevo_estado: EstadoCita) -> Optional[Cita]:
    """Actualiza el estado de una cita existente."""
    cita = _citas.get(cita_id)
    if cita:
        cita.status = nuevo_estado
    return cita


def reprogramar_cita(cita_id: int, nueva_fecha: date, nueva_hora: str) -> Optional[Cita]:
    """Actualiza fecha, hora y estado de una cita existente."""
    cita = _citas.get(cita_id)
    if cita:
        cita.date = nueva_fecha
        cita.time = nueva_hora
        cita.status = EstadoCita.RESCHEDULED
    return cita