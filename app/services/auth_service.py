import bcrypt
from app.domain.auth_model import LoginRequest
from app.domain.user_model import Usuario
from app.repositories import user_repository
from app.core.jwt_handler import crear_token, EXPIRES_IN_SECONDS


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class UsuarioNoEncontradoError(Exception):
    """El correo no corresponde a ningún usuario registrado."""
    pass


class CredencialesInvalidasError(Exception):
    """La contraseña no coincide con el hash almacenado."""
    pass


class UsuarioInactivoError(Exception):
    """El usuario existe pero su cuenta está desactivada."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado durante el proceso de autenticación."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def iniciar_sesion(datos: LoginRequest) -> dict:
    """
    Autentica un usuario y genera un token JWT.

    Reglas de negocio:
    1. El correo debe existir en el sistema         → 404 si no existe
    2. El usuario debe estar activo                 → 403 si está inactivo
    3. La contraseña debe coincidir con el hash     → 401 si no coincide
    4. Se genera un JWT con user_id, rol y exp      → 200 si todo OK

    Lanza:
    - UsuarioNoEncontradoError  → HTTP 404
    - UsuarioInactivoError      → HTTP 403
    - CredencialesInvalidasError → HTTP 401
    - ErrorInternoError         → HTTP 500
    """
    try:
        # Regla 1: el usuario debe existir
        usuario: Usuario | None = user_repository.obtener_por_email(datos.email)
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado")

        # Regla 2: la cuenta debe estar activa
        if not usuario.activo:
            raise UsuarioInactivoError("Usuario inactivo")

        # Regla 3: verificar contraseña contra el hash bcrypt
        password_correcta = bcrypt.checkpw(
            datos.password.encode("utf-8"),
            usuario.password_hash.encode("utf-8"),
        )
        if not password_correcta:
            raise CredencialesInvalidasError("Credenciales incorrectas")

        # Regla 4: generar JWT
        token = crear_token(user_id=usuario.id, rol=usuario.rol.value)

        return {
            "user_id": usuario.id,
            "email": usuario.email,
            "rol": usuario.rol.value,
            "token": token,
            "expires_in": EXPIRES_IN_SECONDS,
        }

    except (UsuarioNoEncontradoError, UsuarioInactivoError, CredencialesInvalidasError):
        raise  # dejar que el router las maneje individualmente

    except Exception as e:
        raise ErrorInternoError("Error al iniciar sesión") from e