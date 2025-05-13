from fastapi import APIRouter, HTTPException
from modelos.modeloAlumno import ModeloCrearAlumno, ModeloActualizarAlumno
from database import Alumno, Alumno_Materia

router = APIRouter()

def buscarAlumno(idAlumno:int):
    alumno = Alumno.select().where(Alumno.id_alumno==idAlumno).first()
    if not alumno:
        raise HTTPException(404,"Alumno no encontrado")
    return alumno

@router.post("/alumno", tags=["Alumno"])
def crear_alumno(alumno_request: ModeloCrearAlumno): #Se pedira un body con los datos definidos en el modelo de crear alumno
    alumno_request = Alumno.create(
        id_alumno = alumno_request.id_alumno,
        nombre_alumno = alumno_request.nombre_alumno,
        apellido_alumno = alumno_request.apellido_alumno,
    )
    return alumno_request

@router.get("/alumnos", tags=["Alumno"])
def get_alumnos():
    alumnos = Alumno.select()
    if not alumnos:
        raise HTTPException(404, "No se encontraron alumnos")
    return [alumno.__data__ for alumno in alumnos] #Convierte cada objeto Peewee en diccionario

@router.get("/alumno/{id}", tags=["Alumno"])
def get_alumno(id_request: int):
    alumno = buscarAlumno(id_request)
    return alumno

@router.put("/alumno/{id}", tags=["Alumno"])
def actualizar_alumno(id_request: int, alumno_actualizado: ModeloActualizarAlumno):
    alumno = buscarAlumno(id_request)
    alumno.nombre_alumno = alumno_actualizado.nombre_alumno
    alumno.apellido_alumno = alumno_actualizado.apellido_alumno
    alumno.save()
    return {"mensaje": "Alumno actualizado", "alumno": alumno.__data__}

@router.delete("/alumno/{id}", tags=["Alumno"])
def delete_alumno(id_request: int):
    alumno = buscarAlumno(id_request)
    Alumno_Materia.delete().where(Alumno_Materia.id_alumno == id_request).execute() #Elimina el registro en Alumno-Materia si es que hay
    alumno.delete_instance()
    return "Alumno eliminado"