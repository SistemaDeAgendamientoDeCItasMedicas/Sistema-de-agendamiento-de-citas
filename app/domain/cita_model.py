from pydantic import BaseModel, field_validator
from datetime import date, datetime, timezone
from datetime import time as Time
from enum import Enum


class EstadoCita(str, Enum):
    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"
    RESCHEDULED = "RESCHEDULED"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"          # ← nuevo para HU-10 (soft delete)


# ─── Entrada ─────────────────────────────────────────────────────────────────

class CitaCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    time: str
    reason: str

    @field_validator("date")
    @classmethod
    def validar_fecha(cls, v: date) -> date:
        if v < datetime.now(timezone.utc).date():
            raise ValueError("Appointments cannot be scheduled in the past")
        return v

    @field_validator("time")
    @classmethod
    def validar_hora(cls, v: str) -> str:
        try:
            hora = datetime.strptime(v, "%H:%M").time()
        except ValueError:
            raise ValueError("Time format must be HH:MM")

        hora_min = Time(8, 0)
        hora_max = Time(18, 0)

        if not (hora_min <= hora <= hora_max):
            raise ValueError("Time must be between 08:00 and 18:00")
        return v

    @field_validator("reason")
    @classmethod
    def validar_motivo(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 5:
            raise ValueError("Reason must be at least 5 characters")
        return v


# ─── Respuesta ───────────────────────────────────────────────────────────────

class CitaData(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    date: str
    time: str
    reason: str
    status: EstadoCita


class CitaResponse(BaseModel):
    message: str
    data: CitaData
    success: bool


class ErrorResponse(BaseModel):
    message: str
    success: bool


# ─── Modelo interno (repositorio) ────────────────────────────────────────────

class Cita(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: date
    time: str
    reason: str
    status: EstadoCita = EstadoCita.SCHEDULED
    created_at: datetime