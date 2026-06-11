from fastapi import APIRouter, HTTPException, status
from app.domain.auth_model import LoginRequest, LoginResponse, LoginData
from app.services import auth_service
from app.services.auth_service import (
    UsuarioNoEncontradoError,
    CredencialesInvalidasError,
    UsuarioInactivoError,
    ErrorInternoError,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["[HU-02] Autenticación"],
)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    summary="[HU-02] Iniciar sesión",
    responses={
        200: {
            "description": "Inicio de sesión exitoso",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Inicio de sesión exitoso",
                        "data": {
                            "user_id": 1,
                            "email": "usuario@email.com",
                            "rol": "USER",
                            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "expires_in": 3600,
                        },
                        "success": True,
                    }
                }
            },
        },
        401: {
            "description": "Contraseña incorrecta",
            "content": {
                "application/json": {
                    "example": {"mensaje": "Credenciales incorrectas", "success": False}
                }
            },
        },
        403: {
            "description": "Usuario inactivo",
            "content": {
                "application/json": {
                    "example": {"mensaje": "Usuario inactivo", "success": False}
                }
            },
        },
        404: {
            "description": "Usuario no encontrado",
            "content": {
                "application/json": {
                    "example": {"mensaje": "Usuario no encontrado", "success": False}
                }
            },
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"mensaje": "Error al iniciar sesión", "success": False}
                }
            },
        },
    },
)
def iniciar_sesion(datos: LoginRequest):
    """
    Autentica un usuario registrado y retorna un token JWT.

    **Validaciones aplicadas:**
    - Email: formato válido y existente en el sistema
    - Contraseña: verificada contra el hash bcrypt almacenado
    - Estado: el usuario debe estar activo

    **Token JWT:**
    - Algoritmo: HS256
    - Contiene: user_id y rol
    - Expiración: 3600 segundos (1 hora)
    """
    try:
        resultado = auth_service.iniciar_sesion(datos)

        return LoginResponse(
            mensaje="Inicio de sesión exitoso",
            data=LoginData(**resultado),
            success=True,
        )

    except UsuarioNoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"mensaje": str(e), "success": False},
        )

    except UsuarioInactivoError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"mensaje": str(e), "success": False},
        )

    except CredencialesInvalidasError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"mensaje": str(e), "success": False},
        )

    except ErrorInternoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"mensaje": str(e), "success": False},
        )