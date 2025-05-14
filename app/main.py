from contextlib import asynccontextmanager
from fastapi import FastAPI
from .rutas import alumnos, profesores, materias, alumno_materia
from .database import myDB 

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Lo siguiente se ejecuta antes de iniciar la aplicación
    if myDB.is_closed():
        myDB.connect()
    yield
    #Lo siguiente se ejecuta antes de apagar la aplicación
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

@app.get("/health")
def health_check():
    return {"status": "ok"}