from fastapi import FastAPI
from app.api.usuarios_api import router as usuarios_router

app = FastAPI()

app.include_router(usuarios_router)