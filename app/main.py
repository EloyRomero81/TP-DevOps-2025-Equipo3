from fastapi import FastAPI
from app.rutas import estudiantes
from app.modelos import Base
from app.base_datos import motor

app = FastAPI()

# Crea las tablas en la base si no existen
Base.metadata.create_all(bind=motor)

# Conectamos nuestras rutas
app.include_router(estudiantes.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de notas de estudiantes"}
