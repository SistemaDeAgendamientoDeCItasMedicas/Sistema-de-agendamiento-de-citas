from app.domain.usuarios_domain import Usuario

class UsuarioRepository:

    def obtener_usuario(self):
        return Usuario(
            nombre="Sebastian",
            correo="sebastian@gmail.com"
        )