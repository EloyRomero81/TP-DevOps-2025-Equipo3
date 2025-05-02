from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.base_datos import SesionLocal
from app import crud, modelos
from app.modelos import EstudianteBD, Estudiante, CrearEstudiante


router = APIRouter()

# Esta función se encarga de abrir y cerrar la sesión con la base
def obtener_bd():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo estudiante (POST /estudiantes/)
@router.post("/estudiantes/", response_model=Estudiante)
def crear_estudiante(estudiante: CrearEstudiante, db: Session = Depends(obtener_bd)):
    nuevo_estudiante = EstudianteBD(nombre=estudiante.nombre, correo=estudiante.correo)
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

# Ver todos los estudiantes (GET /estudiantes/)
@router.get("/estudiantes/", response_model=list[Estudiante])
def leer_estudiantes(db: Session = Depends(obtener_bd)):
    return db.query(EstudianteBD).all()

