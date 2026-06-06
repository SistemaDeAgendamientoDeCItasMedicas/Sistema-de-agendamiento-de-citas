from typing import Optional
from app.domain.user_model import Usuario, UsuarioCreate, RolUsuario
from datetime import datetime, timezone


# ─── Almacenamiento en memoria ───────────────────────────────────────────────
_usuarios: dict[int, Usuario] = {}
_siguiente_id: int = 1


def guardar_usuario(nombre: str, email: str, password_hash: str) -> Usuario:
    """
    Persiste un nuevo usuario en memoria.
    Retorna la entidad creada con ID y fecha de creación asignados.
    """
    global _siguiente_id

    nuevo_usuario = Usuario(
        id=_siguiente_id,
        nombre=nombre,
        email=email,
        password_hash=password_hash,
        rol=RolUsuario.USER,                        # rol por defecto
        activo=True,
        fecha_creacion=datetime.now(timezone.utc),  # fecha de creación automática
    )

    _usuarios[_siguiente_id] = nuevo_usuario
    _siguiente_id += 1
    return nuevo_usuario


def obtener_por_email(email: str) -> Optional[Usuario]:
    """Busca un usuario por email (case-insensitive). Retorna None si no existe."""
    for usuario in _usuarios.values():
        if usuario.email.lower() == email.lower():
            return usuario
    return None


def obtener_por_id(usuario_id: int) -> Optional[Usuario]:
    """Busca un usuario por su ID."""
    return _usuarios.get(usuario_id)


def listar_todos() -> list[Usuario]:
    """Retorna todos los usuarios registrados."""
    return list(_usuarios.values())