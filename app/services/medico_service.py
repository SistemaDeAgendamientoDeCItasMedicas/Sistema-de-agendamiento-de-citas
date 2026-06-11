from app.domain.medico_model import Medico, MedicoCreate
from app.repositories import medico_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class DocumentoYaRegistradoError(Exception):
    """El número de documento ya existe en el sistema."""
    pass


class EmailYaRegistradoError(Exception):
    """El correo ya está asociado a otro médico."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al procesar el registro."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def registrar_medico(datos: MedicoCreate) -> Medico:
    """
    Registra un nuevo médico en el sistema.

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
    if medico_repository.obtener_por_documento(datos.documento):
        raise DocumentoYaRegistradoError(
            f"El documento '{datos.documento}' ya está registrado"
        )

    # Regla 2: email único
    if medico_repository.obtener_por_email(datos.email):
        raise EmailYaRegistradoError(
            f"El correo '{datos.email}' ya está registrado"
        )

    try:
        medico = medico_repository.guardar_medico(datos)
        return medico
    except Exception as e:
        raise ErrorInternoError("Error al registrar médico") from e