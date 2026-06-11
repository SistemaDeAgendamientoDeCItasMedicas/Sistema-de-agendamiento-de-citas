import bcrypt
from app.domain.user_model import Usuario, UsuarioCreate
from app.repositories import user_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class EmailYaRegistradoError(Exception):
    """El correo ya existe en el sistema."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al procesar el registro."""
    pass


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _hashear_password(password: str) -> str:
    """Aplica bcrypt al texto plano y retorna el hash como string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    """Verifica que un texto plano coincida con el hash almacenado."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def registrar_usuario(datos: UsuarioCreate) -> Usuario:
    """
    Registra un nuevo usuario en el sistema.

    Reglas de negocio:
    1. El email debe ser único en el sistema.
    2. La contraseña se hashea con bcrypt antes de almacenar.
    3. Se asigna el rol USER por defecto.
    4. Se registra la fecha de creación automáticamente.

    Lanza:
    - EmailYaRegistradoError  → HTTP 409
    - ErrorInternoError       → HTTP 500
    """
    # Regla 1: email único
    if user_repository.obtener_por_email(datos.email):
        raise EmailYaRegistradoError("El correo ya está registrado")

    try:
        # Regla 2: hashear contraseña
        password_hash = _hashear_password(datos.password)

        # Regla 3 y 4: rol por defecto y fecha de creación (los asigna el repo)
        usuario = user_repository.guardar_usuario(
            nombre=datos.nombre,
            email=datos.email,
            password_hash=password_hash,
        )
        return usuario

    except Exception as e:
        raise ErrorInternoError("Error al registrar usuario") from e