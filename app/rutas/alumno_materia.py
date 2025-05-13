from fastapi import APIRouter, HTTPException
from modelos.modeloAlumnoMateria import ModeloCrearAlumnoMateria, ModeloActualizarAlumnoMateria
from .alumnos import buscarAlumno
from .materias import buscarMateria
from database import Alumno_Materia, Alumno, Materia

router = APIRouter()

#CREAR INSCRIPCION
@router.post("/alumno-materia", tags=["Alumno-Materia"])
def crear_alumno_materia(alumno_materia_request: ModeloCrearAlumnoMateria): #Se pedira un body con los datos definidos en el modelo de crear alumno_materia
    buscarMateria(alumno_materia_request.id_materia)
    buscarAlumno(alumno_materia_request.id_alumno)
    alumno_materia_request = Alumno_Materia.create(
        id_alumno = alumno_materia_request.id_alumno,
        id_materia = alumno_materia_request.id_materia,
        nota_parcial1 = alumno_materia_request.nota_parcial1,
        nota_parcial2 = alumno_materia_request.nota_parcial2,
        nota_final = alumno_materia_request.nota_final,
    )
    return alumno_materia_request

#OBTENER TODOS LOS ALUMNOS DE TODAS LAS MATERIAS
@router.get("/alumnos-materias", tags=["Alumno-Materia"])
def get_alumnos_materias():
    alumnos_materias = (Alumno_Materia.select(Materia.id_materia,Materia.nombre_materia,Alumno.nombre_alumno,Alumno.apellido_alumno)
        .join(Alumno, on=(Alumno_Materia.id_alumno == Alumno.id_alumno))
        .switch(Alumno_Materia)
        .join(Materia, on=(Alumno_Materia.id_materia == Materia.id_materia))
        .order_by(Alumno.id_alumno))
        
    resultado = {} 
    for relacion in alumnos_materias:
        alumno = relacion.id_alumno
        materia = relacion.id_materia

        if materia.id_materia not in resultado: #La primera vez que aparece la materia se inicializa su nombre y el listado de alumnos
            resultado[materia.id_materia] = {
                "Nombre Materia": materia.nombre_materia,
                "Alumnos": []
            }
        resultado[materia.id_materia]["Alumnos"].append({
            "Nombre y Apellido Alumno": alumno.nombre_alumno+" "+alumno.apellido_alumno
        })
    return resultado

#OBTENER TODAS LAS MATERIAS DE UN ALUMNO
@router.get("/alumno-materia/alumno/{id_alumno}", tags=["Alumno-Materia"])
def get_alumno_materia(id_alumno_request: int):
    buscarAlumno(id_alumno_request)
    alumnos_materias = (Alumno_Materia.select(Alumno.id_alumno,Alumno.nombre_alumno,Alumno.apellido_alumno,Materia.nombre_materia)
        .where(Alumno_Materia.id_alumno==id_alumno_request)
        .join(Alumno, on=(Alumno_Materia.id_alumno == Alumno.id_alumno))
        .switch(Alumno_Materia)
        .join(Materia, on=(Alumno_Materia.id_materia == Materia.id_materia))
        .order_by(Alumno.id_alumno))
        
    resultado = {} 
    for relacion in alumnos_materias:
        alumno = relacion.id_alumno
        materia = relacion.id_materia

        if alumno.id_alumno not in resultado:
            resultado[alumno.id_alumno] = {
                "Nombre Alumno": alumno.nombre_alumno,
                "Apellido Alumno": alumno.apellido_alumno,
                "Materias": []
            }
        resultado[alumno.id_alumno]["Materias"].append({ 
            "Nombre Materia": materia.nombre_materia,
            "Nota parcial 1": relacion.nota_parcial1,
            "Nota parcial 2": relacion.nota_parcial2,
            "Nota Final": relacion.nota_final
        })
    return resultado

#OBTENER TODOS LOS ALUMNOS DE UNA MATERIA
@router.get("/alumno-materia/materia/{id_materia}", tags=["Alumno-Materia"])
def get_materia_alumno(id_materia_request: int):
    buscarMateria(id_materia_request)
    alumnos_materias = (Alumno_Materia.select(Materia.id_materia,Materia.nombre_materia,Alumno.nombre_alumno,Alumno.apellido_alumno)
        .where(Alumno_Materia.id_materia==id_materia_request)
        .join(Alumno, on=(Alumno_Materia.id_alumno == Alumno.id_alumno))
        .switch(Alumno_Materia)
        .join(Materia, on=(Alumno_Materia.id_materia == Materia.id_materia))
        .order_by(Alumno.id_alumno))
        
    resultado = {} 
    for relacion in alumnos_materias:
        alumno = relacion.id_alumno
        materia = relacion.id_materia

        if materia.id_materia not in resultado: #La primera vez que aparece la materia se inicializa su nombre y el listado de alumnos
            resultado[materia.id_materia] = {
                "Nombre Materia": materia.nombre_materia,
                "Alumnos": []
            }
        resultado[materia.id_materia]["Alumnos"].append({
            "Nombre y Apellido Alumno": alumno.nombre_alumno+" "+alumno.apellido_alumno
        })
    return resultado

#ACTUALIZAR LAS NOTAS DE LA MATERIA DE UN ALUMNO
@router.put("/alumno-materia/{id_alumno}/{id_materia}", tags=["Alumno-Materia"])
def actualizar_alumno_materia(id_alumno_request: int, id_materia_request: int, alumno_materia_actualizado: ModeloActualizarAlumnoMateria):
    # Validar existencia de alumno y materia
    buscarAlumno(id_alumno_request)
    buscarMateria(id_materia_request)

    relacion = (Alumno_Materia.select().where((Alumno_Materia.id_alumno == id_alumno_request) & (Alumno_Materia.id_materia == id_materia_request)).first())
    if relacion is None:
        raise HTTPException(404, "Relación alumno-materia no encontrada. (No hay inscripción para el alumno en la materia)")

    if alumno_materia_actualizado.nota_parcial1 is not None:
        relacion.nota_parcial1 = alumno_materia_actualizado.nota_parcial1
    if alumno_materia_actualizado.nota_parcial2 is not None:
        relacion.nota_parcial2 = alumno_materia_actualizado.nota_parcial2
    if alumno_materia_actualizado.nota_final is not None:
        relacion.nota_final = alumno_materia_actualizado.nota_final

    relacion.save()
    return "Notas actualizadas correctamente."
   

#ELIMINAR INSCRIPCION
@router.delete("/alumno_materia/{id_alumno}/{id_materia}", tags=["Alumno-Materia"])
def delete_alumno_materia(id_alumno_request: int, id_materia_request: int):
    buscarAlumno(id_alumno_request)
    buscarMateria(id_materia_request)
    alumno_materia = Alumno_Materia.select().where((Alumno_Materia.id_alumno == id_alumno_request) & (Alumno_Materia.id_materia == id_materia_request)).first()
    if alumno_materia is None:
        raise HTTPException(404,"Relación Alumno-Materia no encontrada.")
    alumno_materia.delete_instance()
    return "Relacion Alumno-Materia eliminada"