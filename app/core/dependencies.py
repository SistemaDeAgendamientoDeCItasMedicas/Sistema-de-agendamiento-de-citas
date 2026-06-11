from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.core.jwt_handler import verificar_token

# Esquema Bearer — lee el header Authorization: Bearer <token>
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    Dependencia reutilizable para proteger endpoints con JWT.

    Uso en cualquier router:
        @router.post("/", dependencies=[Depends(get_current_user)])

    O si necesitas los datos del usuario dentro del endpoint:
        def mi_endpoint(usuario: dict = Depends(get_current_user)):
    """
    token = credentials.credentials

    try:
        payload = verificar_token(token)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"mensaje": "Token inválido o expirado", "success": False},
            headers={"WWW-Authenticate": "Bearer"},
        )