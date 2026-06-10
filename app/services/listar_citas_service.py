from app.domain.cita_model import Cita
from app.repositories import cita_repository


# ─── Excepciones de negocio ──────────────────────────────────────────────────

class TamanoPaginaExcedidoError(Exception):
    """El tamaño de página supera el límite permitido de 50."""
    pass


class ErrorInternoError(Exception):
    """Error inesperado al listar las citas."""
    pass


# ─── Constante ───────────────────────────────────────────────────────────────
MAX_PAGE_SIZE = 50


# ─── Caso de uso ─────────────────────────────────────────────────────────────

def listar_citas(page: int, size: int) -> tuple[list[Cita], int]:
    """
    Lista todas las citas con paginación obligatoria.

    Reglas de negocio:
    1. El tamaño máximo de página es 50.
    2. Los resultados se ordenan por fecha y hora ascendente.
    3. Si no hay citas, retorna lista vacía.

    Retorna: (lista_citas, total_registros)

    Lanza:
    - TamanoPaginaExcedidoError → HTTP 400
    - ErrorInternoError         → HTTP 500
    """
    # Regla 1: validar límite de tamaño
    if size > MAX_PAGE_SIZE:
        raise TamanoPaginaExcedidoError(
            f"Page size exceeds maximum allowed limit of {MAX_PAGE_SIZE}"
        )

    try:
        citas, total = cita_repository.listar_con_filtros(
            page=page,
            size=size,
        )
        return citas, total

    except TamanoPaginaExcedidoError:
        raise
    except Exception as e:
        raise ErrorInternoError("Error listing appointments") from e