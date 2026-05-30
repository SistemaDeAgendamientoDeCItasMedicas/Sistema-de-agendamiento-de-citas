from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.user_router import router as usuario_router
from app.api.auth_router import router as auth_router

app = FastAPI(
    title="Sistema de Agendamiento de Citas Médicas",
    description="API REST para gestión de citas médicas — Arquitectura por capas",
    version="1.0.0",
)

# ─── Manejador errores de validación Pydantic → formato { mensaje, success } ─
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = exc.errors()
    primer_error = errores[0] if errores else {}
    campo = " → ".join(str(x) for x in primer_error.get("loc", []))
    mensaje = primer_error.get("msg", "Datos inválidos")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"mensaje": f"{mensaje} (campo: {campo})", "success": False},
    )


# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(usuario_router)
app.include_router(auth_router)


# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Sistema de Agendamiento de Citas Médicas — API activa",
        "version": "1.0.0",
        "docs": "/docs",
    }


# ─── Routers ─────────────────────────────────────────────────────────────────
app.include_router(usuario_router)


# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Sistema de Agendamiento de Citas Médicas — API activa",
        "version": "1.0.0",
        "docs": "/docs",
    }