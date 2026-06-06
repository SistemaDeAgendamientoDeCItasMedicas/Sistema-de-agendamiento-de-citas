from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# ─── Configuración JWT ────────────────────────────────────────────────────────
# En producción estos valores van en variables de entorno (.env)
SECRET_KEY = "clave-secreta-sistema-citas-medicas-2024"
ALGORITHM = "HS256"
EXPIRES_IN_SECONDS = 3600  # 1 hora


def crear_token(user_id: int, rol: str) -> str:
    """
    Genera un JWT firmado con user_id, rol y tiempo de expiración.
    """
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),       # subject — identificador del usuario
        "rol": rol,
        "iat": ahora,              # issued at
        "exp": ahora + timedelta(seconds=EXPIRES_IN_SECONDS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str) -> dict:
    """
    Decodifica y valida un JWT.
    Retorna el payload si es válido, lanza JWTError si no.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])