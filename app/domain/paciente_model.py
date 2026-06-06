from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from enum import Enum
import re


class EstadoPaciente(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


# ─── Entrada ─────────────────────────────────────────────────────────────────

class PacienteCreate(BaseModel):
    nombre: str
    documento: str
    email: EmailStr
    telefono: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        return v

    @field_validator("documento")
    @classmethod
    def validar_documento(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit():
            raise ValueError("El documento debe contener solo números")
        if not (6 <= len(v) <= 12):
            raise ValueError("El documento debe tener entre 6 y 12 dígitos")
        return v

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^\+?[0-9]{7,15}$", v):
            raise ValueError("El teléfono debe contener entre 7 y 15 dígitos numéricos")
        return v


# ─── Respuesta ───────────────────────────────────────────────────────────────

class PacienteData(BaseModel):
    paciente_id: int
    nombre: str
    documento: str
    estado: EstadoPaciente


class PacienteResponse(BaseModel):
    mensaje: str
    data: PacienteData
    success: bool


class ErrorResponse(BaseModel):
    mensaje: str
    success: bool


# ─── Modelo interno (repositorio) ────────────────────────────────────────────

class Paciente(BaseModel):
    id: int
    nombre: str
    documento: str
    email: str
    telefono: str
    estado: EstadoPaciente = EstadoPaciente.ACTIVO
    fecha_creacion: datetime