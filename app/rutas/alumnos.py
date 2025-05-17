from fastapi import APIRouter, HTTPException
from starlette import status
from app.modelos.modeloAlumno import ModeloCrearAlumno, ModeloActualizarAlumno
from app.database import Alumno, Alumno_Materia

router = APIRouter()


def buscarAlumno(idAlumno: int):
    alumno = Alumno.select().where(Alumno.id_alumno == idAlumno).first()
    if not alumno:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alumno no encontrado")
    return alumno


@router.post("/alumno", tags=["Alumno"], status_code=status.HTTP_201_CREATED)
def crear_alumno(
    alumno_request: ModeloCrearAlumno,
):  # Se pedira un body con los datos definidos en el modelo de crear alumno
    alumno_request = Alumno.create(
        id_alumno=alumno_request.id_alumno,
        nombre_alumno=alumno_request.nombre_alumno,
        apellido_alumno=alumno_request.apellido_alumno,
    )
    return alumno_request


@router.get("/alumnos", tags=["Alumno"])
def get_alumnos():
    alumnos = Alumno.select()
    if not alumnos:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No se encontraron alumnos")
    return [
        alumno.__data__ for alumno in alumnos
    ]  # Convierte cada objeto Peewee en diccionario


@router.get("/alumno/{id}", tags=["Alumno"])
def get_alumno(id: int):
    alumno = buscarAlumno(id)
    return alumno


@router.put("/alumno/{id}", tags=["Alumno"], status_code=status.HTTP_200_OK)
def actualizar_alumno(id: int, alumno_actualizado: ModeloActualizarAlumno):
    alumno = buscarAlumno(id)
    alumno.nombre_alumno = alumno_actualizado.nombre_alumno
    alumno.apellido_alumno = alumno_actualizado.apellido_alumno
    alumno.save()
    return {"mensaje": "Alumno actualizado", "alumno": alumno.__data__}


@router.delete("/alumno/{id}", tags=["Alumno"], status_code=status.HTTP_200_OK)
def delete_alumno(id: int):
    alumno = buscarAlumno(id)
    Alumno_Materia.delete().where(
        Alumno_Materia.id_alumno == id
    ).execute()  # Elimina el registro en Alumno-Materia si es que hay
    alumno.delete_instance()
    return "Alumno eliminado"
