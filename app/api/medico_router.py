from fastapi import APIRouter, HTTPException, status, Depends
from app.domain.medico_model import MedicoCreate, MedicoResponse, MedicoData
from app.services import medico_service
from app.services.medico_service import (
    DocumentoYaRegistradoError,
    EmailYaRegistradoError,
    ErrorInternoError,
)
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/medicos",
    tags=["[HU-04] Registro de Médico"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=MedicoResponse,
    summary="[HU-04] Registrar médico",
    responses={
        201: {
            "description": "Médico registrado correctamente",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Médico registrado correctamente",
                        "data": {
                            "medico_id": 1,
                            "nombre": "Dr. Juan Perez",
                            "documento": "87654321",
                            "especialidad": "CARDIOLOGIA",
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
                        "mensaje": "Error al registrar médico",
                        "success": False,
                    }
                }
            },
        },
    },
)
def registrar_medico(
    datos: MedicoCreate,
    usuario_actual: dict = Depends(get_current_user),
):
    """
    Registra un nuevo médico en el sistema.

    **Requiere autenticación:** Bearer Token JWT (obtenido en HU-02 login).

    **Validaciones aplicadas:**
    - Nombre: mínimo 2 caracteres
    - Documento: solo números, entre 6 y 12 dígitos, único en el sistema
    - Email: formato válido y único en el sistema
    - Teléfono: entre 7 y 15 dígitos numéricos
    - Especialidad: valor del listado permitido

    **Especialidades disponibles:**
    MEDICINA_GENERAL | PEDIATRIA | CARDIOLOGIA | DERMATOLOGIA |
    GINECOLOGIA | NEUROLOGIA | ORTOPEDIA | PSIQUIATRIA

    **Estado inicial asignado:** `ACTIVO`
    """
    try:
        medico = medico_service.registrar_medico(datos)

        return MedicoResponse(
            mensaje="Médico registrado correctamente",
            data=MedicoData(
                medico_id=medico.id,
                nombre=medico.nombre,
                documento=medico.documento,
                especialidad=medico.especialidad,
                estado=medico.estado,
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