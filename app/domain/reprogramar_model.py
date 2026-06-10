from pydantic import BaseModel, field_validator
from datetime import date, datetime, timezone
from datetime import time as Time


# ─── Entrada ─────────────────────────────────────────────────────────────────

class ReprogramarCitaRequest(BaseModel):
    date: date
    time: str

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