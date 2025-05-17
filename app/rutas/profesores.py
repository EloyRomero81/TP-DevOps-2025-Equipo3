from fastapi import APIRouter, HTTPException
from starlette import status
from app.modelos.modeloProfesor import ModeloCrearProfesor, ModeloActualizarProfesor
from app.database import Profesor

router = APIRouter()


def buscarProfesor(idProfesor: int):
    profesor = Profesor.select().where(Profesor.id_profesor == idProfesor).first()
    if not profesor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profesor no encontrado")
    return profesor


@router.post("/profesor", tags=["Profesor"], status_code=status.HTTP_201_CREATED)
def crear_profesor(
    nuevo_profesor: ModeloCrearProfesor,
):  # Se pedira un body con los datos definidos en el modelo de crear profesor
    nuevo_profesor = Profesor.create(
        id_profesor=nuevo_profesor.id_profesor,
        nombre_profesor=nuevo_profesor.nombre_profesor,
        apellido_profesor=nuevo_profesor.apellido_profesor,
    )
    return nuevo_profesor


@router.get("/profesores", tags=["Profesor"], status_code=status.HTTP_200_OK)
def get_profesores():
    profesores = Profesor.select()
    if not profesores:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No se encontraron profesores")
    return [
        profesor.__data__ for profesor in profesores
    ]  # Convierte cada objeto Peewee en diccionario


@router.get("/profesor/{id}", tags=["Profesor"], status_code=status.HTTP_200_OK)
def get_profesor(id: int):
    profesor = buscarProfesor(id)
    return profesor


@router.put("/profesor/{id}", tags=["Profesor"], status_code=status.HTTP_200_OK)
def actualizar_profesor(id: int, profesor_actualizado: ModeloActualizarProfesor):
    profesor = buscarProfesor(id)
    profesor.nombre_profesor = profesor_actualizado.nombre_profesor
    profesor.apellido_profesor = profesor_actualizado.apellido_profesor
    profesor.save()
    return {"mensaje": "Profesor actualizado", "profesor": profesor.__data__}


@router.delete("/profesor/{id}", tags=["Profesor"], status_code=status.HTTP_200_OK)
def delete_profesor(id: int):
    profesor = buscarProfesor(
        id
    )  # Seguro salta error si se elimina un profe relacionado una materia
    profesor.delete_instance()
    return "Profesor eliminado"
