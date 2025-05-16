from fastapi import APIRouter, HTTPException
from starlette import status
from app.modelos.modeloMateria import ModeloCrearMateria, ModeloActualizarMateria
from .profesores import buscarProfesor
from app.database import Materia, Alumno_Materia

router = APIRouter()

def buscarMateria(idMateria:int):
    materia = Materia.select().where(Materia.id_materia==idMateria).first()
    if not materia:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Materia no encontrada")
    return materia

@router.post("/materia", tags=["Materia"], status_code=status.HTTP_201_CREATED)
def crear_materia(nueva_materia: ModeloCrearMateria): #Se pedira un body con los datos definidos en el modelo de crear materia
    buscarProfesor(nueva_materia.id_profesor)
    nueva_materia = Materia.create(
        id_materia = nueva_materia.id_materia,
        nombre_materia = nueva_materia.nombre_materia,
        id_profesor = nueva_materia.id_profesor,
    )
    return nueva_materia

@router.get("/materias", tags=["Materia"], status_code=status.HTTP_200_OK)
def get_materias():
    materias = Materia.select()
    if not materias:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No se encontraron materias")
    return [materia.__data__ for materia in materias] #Convierte cada objeto Peewee en diccionario

@router.get("/materia/{id}", tags=["Materia"], status_code=status.HTTP_200_OK)
def get_materia(id: int):
    materia = buscarMateria(id)
    return materia

@router.put("/materia/{id}", tags=["Materia"], status_code=status.HTTP_200_OK)
def actualizar_materia(id: int, materia_actualizado: ModeloActualizarMateria):
    materia = buscarMateria(id) 
    if materia_actualizado.id_profesor is not None:  #Si se envió un nuevo ID de profesor, validar que exista
        buscarProfesor(materia_actualizado.id_profesor)
        materia.id_profesor = materia_actualizado.id_profesor
    if materia_actualizado.nombre_materia is not None:  #Actualizar el nombre de la materia si fue enviado
        materia.nombre_materia = materia_actualizado.nombre_materia

    materia.save()
    return {"mensaje": "Materia actualizada", "Materia": materia.__data__}


@router.delete("/materia/{id}", tags=["Materia"], status_code=status.HTTP_200_OK)
def delete_materia(id: int):
    materia = buscarMateria(id)
    Alumno_Materia.delete().where(Alumno_Materia.id_materia == id).execute() #Elimina el registro en Alumno-Materia si es que hay
    materia.delete_instance()
    return "Materia eliminada"