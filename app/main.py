from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import myDB
from app.rutas import alumnos, profesores, materias, alumno_materia


@asynccontextmanager
async def lifespan(app: FastAPI):
    if myDB.is_closed():
        myDB.connect()
    yield
    if not myDB.is_closed():
        myDB.close()


app = FastAPI(lifespan=lifespan)
app.include_router(alumnos.router)
app.include_router(profesores.router)
app.include_router(materias.router)
app.include_router(alumno_materia.router)


@app.get("/")
def index():
    return {"message": "Bienvenido a la API de notas de estudiantes"}
