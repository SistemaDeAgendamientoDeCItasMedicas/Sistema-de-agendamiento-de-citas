from typing import Optional
from datetime import datetime, timezone
from app.domain.paciente_model import Paciente, PacienteCreate, EstadoPaciente


# ─── Almacenamiento en memoria ───────────────────────────────────────────────
_pacientes: dict[int, Paciente] = {}
_siguiente_id: int = 1


def guardar_paciente(datos: PacienteCreate) -> Paciente:
    """Persiste un nuevo paciente y retorna la entidad creada."""
    global _siguiente_id

    nuevo = Paciente(
        id=_siguiente_id,
        nombre=datos.nombre,
        documento=datos.documento,
        email=datos.email,
        telefono=datos.telefono,
        estado=EstadoPaciente.ACTIVO,
        fecha_creacion=datetime.now(timezone.utc),
    )

    _pacientes[_siguiente_id] = nuevo
    _siguiente_id += 1
    return nuevo


def obtener_por_documento(documento: str) -> Optional[Paciente]:
    """Busca un paciente por número de documento."""
    for paciente in _pacientes.values():
        if paciente.documento == documento:
            return paciente
    return None


def obtener_por_email(email: str) -> Optional[Paciente]:
    """Busca un paciente por correo electrónico."""
    for paciente in _pacientes.values():
        if paciente.email.lower() == email.lower():
            return paciente
    return None


def obtener_por_id(paciente_id: int) -> Optional[Paciente]:
    """Busca un paciente por su ID."""
    return _pacientes.get(paciente_id)


def listar_todos() -> list[Paciente]:
    """Retorna todos los pacientes registrados."""
    return list(_pacientes.values())