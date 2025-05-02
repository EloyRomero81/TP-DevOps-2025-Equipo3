from sqlalchemy.orm import Session
from app.modelos import EstudianteBD, CrearEstudiante

# CREAR un estudiante
def crear_estudiante(db: Session, estudiante: CrearEstudiante):
    estudiante_nuevo = EstudianteBD(nombre=estudiante.nombre, correo=estudiante.correo)
    db.add(estudiante_nuevo)
    db.commit()         # Guarda en la base
    db.refresh(estudiante_nuevo)   # Actualiza con el nuevo ID asignado
    return estudiante_nuevo

# LEER todos los estudiantes
def obtener_estudiantes(db: Session):
    return db.query(EstudianteBD).all()
