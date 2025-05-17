from contextlib import asynccontextmanager
from fastapi import FastAPI
import sentry_sdk
from app.database import myDB
from app.rutas import alumnos, profesores, materias, alumno_materia


sentry_sdk.init(
    dsn="https://6fa54768074effba2a629f76cf39ac4b@o4509339935965184.ingest.de.sentry.io/4509339938127952",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)


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


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
    