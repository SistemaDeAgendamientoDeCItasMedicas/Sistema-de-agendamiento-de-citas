from fastapi import APIRouter, HTTPException, status, Depends
from app.domain.paciente_model import PacienteCreate, PacienteResponse, PacienteData
from app.services import paciente_service
from app.services.paciente_service import (
    DocumentoYaRegistradoError,
    EmailYaRegistradoError,
    ErrorInternoError,
)
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/pacientes",
    tags=["[HU-03] Registro de Paciente"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PacienteResponse,
    summary="[HU-03] Registrar paciente",
    responses={
        201: {
            "description": "Paciente registrado correctamente",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Paciente registrado correctamente",
                        "data": {
                            "paciente_id": 1,
                            "nombre": "Maria Lopez",
                            "documento": "123456789",
                            "estado": "ACTIVO",
                        },
                        "success": True,
                    }
                }
            },
        },
        409: {
            "description": "Documento o correo ya registrado",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "El documento ya está registrado",
                        "success": False,
                    }
                }
            },
        },
        400: {
            "description": "Validación de campos fallida",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "El documento debe contener solo números (campo: documento)",
                        "success": False,
                    }
                }
            },
        },
        401: {
            "description": "Token inválido o no enviado",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Token inválido o expirado",
                        "success": False,
                    }
                }
            },
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Error al registrar paciente",
                        "success": False,
                    }
                }
            },
        },
    },
)
def registrar_paciente(
    datos: PacienteCreate,
    usuario_actual: dict = Depends(get_current_user),  # ← protección JWT
):
    """
    Registra un nuevo paciente en el sistema.

    **Requiere autenticación:** Bearer Token JWT (obtenido en HU-02 login).

    **Validaciones aplicadas:**
    - Nombre: mínimo 2 caracteres
    - Documento: solo números, entre 6 y 12 dígitos, único en el sistema
    - Email: formato válido y único en el sistema
    - Teléfono: entre 7 y 15 dígitos numéricos

    **Estado inicial asignado:** `ACTIVO`
    """
    try:
        paciente = paciente_service.registrar_paciente(datos)

        return PacienteResponse(
            mensaje="Paciente registrado correctamente",
            data=PacienteData(
                paciente_id=paciente.id,
                nombre=paciente.nombre,
                documento=paciente.documento,
                estado=paciente.estado,
            ),
            success=True,
        )

    except DocumentoYaRegistradoError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"mensaje": str(e), "success": False},
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