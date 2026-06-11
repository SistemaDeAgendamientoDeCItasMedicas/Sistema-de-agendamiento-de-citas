from datetime import date
from typing import Optional
from app.domain.cita_model import Cita, EstadoCita
from app.repositories import cita_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class FormatoFechaInvalidoError(Exception):
    """El formato de fecha no es válido."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al consultar las citas."""
    pass


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def consultar_citas(
    date_filter: Optional[date] = None,
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    status: Optional[EstadoCita] = None,
    page: int = 1,
    size: int = 10,
) -> tuple[list[Cita], int]:
    """
    Consulta citas con filtros opcionales y paginación.

    Reglas de negocio:
    1. Todos los filtros son opcionales.
    2. Los resultados se ordenan por fecha y hora ascendente.
    3. Se aplica paginación con page y size.
    4. Si no hay resultados, retorna lista vacía.

    Retorna: (lista_citas, total_registros)

    Lanza:
    - ErrorInternoError → HTTP 500
    """
    try:
        citas, total = cita_repository.listar_con_filtros(
            date_filter=date_filter,
            patient_id=patient_id,
            doctor_id=doctor_id,
            status=status,
            page=page,
            size=size,
        )
        return citas, total

    except Exception as e:
        raise ErrorInternoError("Error retrieving appointments") from e