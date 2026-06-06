from pydantic import BaseModel, EmailStr


# ─── Entrada ─────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ─── Respuesta ───────────────────────────────────────────────────────────────

class LoginData(BaseModel):
    user_id: int
    email: str
    rol: str
    token: str
    expires_in: int


class LoginResponse(BaseModel):
    mensaje: str
    data: LoginData
    success: bool


class ErrorResponse(BaseModel):
    mensaje: str
    success: bool