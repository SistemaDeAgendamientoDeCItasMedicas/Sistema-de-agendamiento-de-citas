from typing import Optional
from datetime import datetime, timezone
from app.domain.medico_model import Medico, MedicoCreate, EstadoMedico


# ─── Almacenamiento en memoria ───────────────────────────────────────────────
_medicos: dict[int, Medico] = {}
_siguiente_id: int = 1


def guardar_medico(datos: MedicoCreate) -> Medico:
    """Persiste un nuevo médico y retorna la entidad creada."""
    global _siguiente_id

    nuevo = Medico(
        id=_siguiente_id,
        nombre=datos.nombre,
        documento=datos.documento,
        email=datos.email,
        telefono=datos.telefono,
        especialidad=datos.especialidad,
        estado=EstadoMedico.ACTIVO,
        fecha_creacion=datetime.now(timezone.utc),
    )

    _medicos[_siguiente_id] = nuevo
    _siguiente_id += 1
    return nuevo


def obtener_por_documento(documento: str) -> Optional[Medico]:
    """Busca un médico por número de documento."""
    for medico in _medicos.values():
        if medico.documento == documento:
            return medico
    return None


def obtener_por_email(email: str) -> Optional[Medico]:
    """Busca un médico por correo electrónico."""
    for medico in _medicos.values():
        if medico.email.lower() == email.lower():
            return medico
    return None


def obtener_por_id(medico_id: int) -> Optional[Medico]:
    """Busca un médico por su ID."""
    return _medicos.get(medico_id)


def listar_todos() -> list[Medico]:
    """Retorna todos los médicos registrados."""
    return list(_medicos.values())