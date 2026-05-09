from app.repositories.usuarios_repository import UsuarioRepository

class UsuarioService:

    def __init__(self):
        self.repository = UsuarioRepository()

    def listar_usuario(self):
        return self.repository.obtener_usuario()