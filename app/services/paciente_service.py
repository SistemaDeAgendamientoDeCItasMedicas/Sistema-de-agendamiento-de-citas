from app.domain.paciente_model import Paciente, PacienteCreate
from app.repositories import paciente_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class DocumentoYaRegistradoError(Exception):
    """El número de documento ya existe en el sistema."""
    pass


class EmailYaRegistradoError(Exception):
    """El correo ya está asociado a otro paciente."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al procesar el registro."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def registrar_paciente(datos: PacienteCreate) -> Paciente:
    """
    Registra un nuevo paciente en el sistema.

    Reglas de negocio:
    1. El documento debe ser único en el sistema.
    2. El correo debe ser único en el sistema.
    3. El estado inicial es ACTIVO automáticamente.
    4. La fecha de creación se asigna automáticamente.

    Lanza:
    - DocumentoYaRegistradoError  → HTTP 409
    - EmailYaRegistradoError      → HTTP 409
    - ErrorInternoError           → HTTP 500
    """
    # Regla 1: documento único
    if paciente_repository.obtener_por_documento(datos.documento):
        raise DocumentoYaRegistradoError(
            f"El documento '{datos.documento}' ya está registrado"
        )

    # Regla 2: email único
    if paciente_repository.obtener_por_email(datos.email):
        raise EmailYaRegistradoError(
            f"El correo '{datos.email}' ya está registrado"
        )

    try:
        paciente = paciente_repository.guardar_paciente(datos)
        return paciente
    except Exception as e:
        raise ErrorInternoError("Error al registrar paciente") from e