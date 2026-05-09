from fastapi import APIRouter
from app.services.usuarios_service import UsuarioService

router = APIRouter()

service = UsuarioService()

@router.get("/usuarios")
def obtener_usuario():

    usuario = service.listar_usuario()

    return {
        "nombre": usuario.nombre,
        "correo": usuario.correo
    }