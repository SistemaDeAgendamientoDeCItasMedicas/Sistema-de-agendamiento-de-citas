from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from enum import Enum
import re


class RolUsuario(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MEDICO = "MEDICO"


# ─── Entrada ────────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        return v

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("La contraseña debe contener al menos una letra")
        if not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v


# ─── Respuesta ───────────────────────────────────────────────────────────────

class UsuarioData(BaseModel):
    user_id: int
    email: str
    rol: RolUsuario


class UsuarioResponse(BaseModel):
    mensaje: str
    data: UsuarioData
    success: bool


class ErrorResponse(BaseModel):
    mensaje: str
    success: bool


# ─── Modelo interno (repositorio) ────────────────────────────────────────────

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    password_hash: str          # contraseña hasheada con bcrypt
    rol: RolUsuario
    activo: bool = True
    fecha_creacion: datetime