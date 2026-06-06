from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from enum import Enum
import re


class EstadoMedico(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


class Especialidad(str, Enum):
    MEDICINA_GENERAL = "MEDICINA_GENERAL"
    PEDIATRIA = "PEDIATRIA"
    CARDIOLOGIA = "CARDIOLOGIA"
    DERMATOLOGIA = "DERMATOLOGIA"
    GINECOLOGIA = "GINECOLOGIA"
    NEUROLOGIA = "NEUROLOGIA"
    ORTOPEDIA = "ORTOPEDIA"
    PSIQUIATRIA = "PSIQUIATRIA"


# ─── Entrada ─────────────────────────────────────────────────────────────────

class MedicoCreate(BaseModel):
    nombre: str
    documento: str
    email: EmailStr
    telefono: str
    especialidad: Especialidad

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

class MedicoData(BaseModel):
    medico_id: int
    nombre: str
    documento: str
    especialidad: Especialidad
    estado: EstadoMedico


class MedicoResponse(BaseModel):
    mensaje: str
    data: MedicoData
    success: bool


class ErrorResponse(BaseModel):
    mensaje: str
    success: bool


# ─── Modelo interno (repositorio) ────────────────────────────────────────────

class Medico(BaseModel):
    id: int
    nombre: str
    documento: str
    email: str
    telefono: str
    especialidad: Especialidad
    estado: EstadoMedico = EstadoMedico.ACTIVO
    fecha_creacion: datetime