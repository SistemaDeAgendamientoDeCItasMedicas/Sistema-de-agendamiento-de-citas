from fastapi import APIRouter, HTTPException, status
from app.domain.user_model import UsuarioCreate, UsuarioResponse, ErrorResponse, UsuarioData
from app.services import user_service
from app.services.user_service import EmailYaRegistradoError, ErrorInternoError

router = APIRouter(
    prefix="/api/v1/users",
    tags=["[HU-01] Registro de Usuario"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UsuarioResponse,
    summary="[HU-01] Registrar usuario",
    responses={
        201: {
            "description": "Usuario registrado correctamente",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Usuario registrado correctamente",
                        "data": {
                            "user_id": 1,
                            "email": "usuario@email.com",
                            "rol": "USER"
                        },
                        "success": True
                    }
                }
            }
        },
        409: {
            "description": "El correo ya está registrado",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "El correo ya está registrado",
                        "success": False
                    }
                }
            }
        },
        400: {
            "description": "Validación de campos fallida",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "La contraseña no cumple los requisitos de seguridad",
                        "success": False
                    }
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Error al registrar usuario",
                        "success": False
                    }
                }
            }
        },
    }
)
def registrar_usuario(datos: UsuarioCreate):
    """
    Registra un nuevo usuario en el sistema.

    **Validaciones aplicadas:**
    - Nombre: mínimo 2 caracteres
    - Email: formato válido y único en el sistema
    - Contraseña: mínimo 8 caracteres, debe combinar letras y números

    **Política de contraseñas:**
    La contraseña debe cumplir todas las siguientes condiciones:
    - Mínimo 8 caracteres
    - Al menos una letra (mayúscula o minúscula)
    - Al menos un número

    **Rol asignado por defecto:** `USER`
    """
    try:
        usuario = user_service.registrar_usuario(datos)

        return UsuarioResponse(
            mensaje="Usuario registrado correctamente",
            data=UsuarioData(
                user_id=usuario.id,
                email=usuario.email,
                rol=usuario.rol,
            ),
            success=True,
        )

    except EmailYaRegistradoError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"mensaje": str(e), "success": False},
        )

    except ErrorInternoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"mensaje": str(e), "success": False},
        )