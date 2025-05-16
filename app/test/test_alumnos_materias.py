import pytest
from fastapi.testclient import TestClient
from starlette import status
from typing import Optional
from app.database import Materia, Profesor, Alumno_Materia, Alumno, set_database, db_prueba, myDB
from app.main import app

@pytest.fixture(scope="function", autouse=True)
def client():        
    set_database(db_prueba)  #Se cambia a la BD de testeo
    if db_prueba.is_closed():
        db_prueba.connect()    
    db_prueba.create_tables([Materia, Profesor, Alumno_Materia, Alumno])
    with TestClient(app) as c:
        yield c
    db_prueba.drop_tables([Materia, Profesor, Alumno_Materia, Alumno])
    db_prueba.close()
    set_database(myDB) #Se restaura a la BD original

def crearProfe(client, idProfe:int, nomProfe:str, apeProfe:str):
    client.post("/profesor", json={
        "id_profesor": idProfe,
        "nombre_profesor": nomProfe,
        "apellido_profesor": apeProfe
    })

def crearMateria(client, idMateria:int, nomMateria:str, idProfe:int):
    client.post("/materia", json={
        "id_materia": idMateria,
        "nombre_materia": nomMateria,
        "id_profesor": idProfe
    })

def crearAlumno(client, idAlumno:int, nomAlumno:str, apeAlumno:str):
    client.post("/alumno", json={
        "id_alumno": idAlumno,
        "nombre_alumno": nomAlumno,
        "apellido_alumno": apeAlumno
    })

def crearAlumnoMateriaSinNotas(client, idMateria:int, idAlumno:int):
    client.post("/alumno-materia", json={
        "id_alumno": idAlumno,
        "id_materia": idMateria,
    })

#Test CRUD

def test_crear_inscripcion_alumno_materia(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,1,"Matematica",3)
    crearAlumno(client,1,"Roberto","Juanes")
    response = client.post("/alumno-materia", json={
        "id_alumno": 1,
        "id_materia": 1,
        "nota_parcial2": 5,
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()["__data__"]
    assert data["id_materia"] == 1
    assert data["id_alumno"] == 1
    assert data["nota_parcial2"] == 5


def test_obtener_todos_alumnos_materias(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,1,"Matematica",3)
    crearMateria(client,2,"Lengua",3)
    crearAlumno(client,1,"Roberto","Juanes")
    crearAlumno(client,2,"Alejandro","Lernes")
    crearAlumnoMateriaSinNotas(client,1,1)
    crearAlumnoMateriaSinNotas(client,2,1)
    crearAlumnoMateriaSinNotas(client,2,2)
    response = client.get("/alumnos-materias")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 2
    assert data["1"]["Nombre Materia"] == "Matematica"
    assert data["1"]["Alumnos"][0]["Nombre y Apellido Alumno"] == "Roberto Juanes"
    assert data["2"]["Nombre Materia"] == "Lengua"
    assert data["2"]["Alumnos"][0]["Nombre y Apellido Alumno"] == "Roberto Juanes"
    assert data["2"]["Alumnos"][1]["Nombre y Apellido Alumno"] == "Alejandro Lernes"
    

def test_obtener_materias_de_alumno(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,1,"Matematica",3)
    crearMateria(client,2,"Lengua",3)
    crearAlumno(client,1,"Roberto","Juanes")
    crearAlumnoMateriaSinNotas(client,1,1)
    crearAlumnoMateriaSinNotas(client,2,1)
    response = client.get("/alumno-materia/alumno/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 1
    assert data["1"]["Nombre Alumno"] == "Roberto"
    assert data["1"]["Apellido Alumno"] == "Juanes"
    assert data["1"]["Materias"][0]["Nombre Materia"] == "Matematica"
    assert data["1"]["Materias"][0]["Nota parcial 1"] == None
    assert data["1"]["Materias"][1]["Nombre Materia"] == "Lengua"
    assert data["1"]["Materias"][1]["Nota Final"] == None

def test_obtener_alumnos_de_materia(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,1,"Matematica",3)
    crearAlumno(client,1,"Roberto","Juanes")
    crearAlumno(client,2,"Juan","Domingo")
    crearAlumnoMateriaSinNotas(client,1,1)
    crearAlumnoMateriaSinNotas(client,1,2)
    response = client.get("/alumno-materia/materia/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 1
    assert data["1"]["Nombre Materia"] == "Matematica"
    assert data["1"]["Alumnos"][0]["Nombre y Apellido Alumno"] == "Roberto Juanes"
    assert data["1"]["Alumnos"][1]["Nombre y Apellido Alumno"] == "Juan Domingo"

def test_actualizar_notas_alumno_materia(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,1,"Matematica",3)
    crearAlumno(client,2,"Juan","Domingo")
    crearAlumnoMateriaSinNotas(client,1,2)
    response = client.put("/alumno-materia/2/1", json={
        "nota_parcial1": 10,
        "nota_parcial2": 8,
        "nota_final": 9,
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["__data__"]
    assert data["id_alumno"] == 2
    assert data["id_materia"] == 1
    assert data["nota_parcial1"] == 10
    assert data["nota_parcial2"] == 8
    assert data["nota_final"] == 9


def test_eliminar_inscripcion_alumno_materia(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,1,"Ciencia sociales",3)
    crearAlumno(client,2,"Juan","Domingo")
    crearAlumnoMateriaSinNotas(client,1,2)
    response = client.delete("/alumno-materia/2/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Relacion Alumno-Materia eliminada"

# Test errores

def test_obtener_todos_alumnos_materias_vacio(client):
    response = client.get("/alumnos-materias")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Inscripciones Alumno-Materia no encontrados"

def test_obtener_inscripcion_inexistente_con_alumno(client):
    crearAlumno(client,2,"Juan","Domingo")
    response = client.get("/alumno-materia/alumno/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No se encontraron materias inscriptas para el alumno"

def test_obtener_inscripcion_inexistente_con_materia(client):
    crearProfe(client,3,"Santiago","Morales")
    crearMateria(client,4,"Ciencia sociales",3)
    response = client.get("/alumno-materia/materia/4")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No se encontraron alumnos incriptos a la materia"

def test_actualizar_inscripcion_inexistente(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,2,"Ciencia sociales",3)
    crearAlumno(client,1,"Juan","Domingo")
    response = client.put("/alumno-materia/1/2", json={
        "nota_parcial1": 10,
        "nota_parcial2": 8
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Inscripción alumno-materia no encontrada. (No hay inscripción para el alumno en la materia)"

def test_eliminar_inscripcion_inexistente(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,2,"Ciencia sociales",3)
    crearAlumno(client,1,"Juan","Domingo")
    response = client.delete("/alumno-materia/1/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Inscripción Alumno-Materia no encontrada"