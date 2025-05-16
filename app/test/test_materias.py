import pytest
from fastapi.testclient import TestClient
from starlette import status
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

#Test CRUD

def test_crear_materia(client):
    crearProfe(client,3,"Enrique","Sosa")
    response = client.post("/materia", json={
        "id_materia": 1,
        "nombre_materia": "Matematica",
        "id_profesor": 3
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()["__data__"]
    assert data["id_materia"] == 1
    assert data["nombre_materia"] == "Matematica"
    assert data["id_profesor"] == 3

def test_obtener_todas_materias(client):
    crearProfe(client,3,"Alberto","Vilda")
    crearMateria(client,1,"Ciencias",3)
    crearMateria(client,2,"Biología",3)
    response = client.get("/materias")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id_materia"] == 1
    assert data[1]["nombre_materia"] == "Biología"
    

def test_obtener_materia_por_id(client):
    crearProfe(client,3,"Enrique","Sosa")
    crearMateria(client,2,"Álgebra",3)
    response = client.get("/materia/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["__data__"]
    assert data["id_materia"] == 2
    assert data["nombre_materia"] == "Álgebra"


def test_actualizar_materia(client):
    crearProfe(client,2,"Juanes","Montoya")
    crearMateria(client,2,"Álgebra",2)
    response = client.put("/materia/2", json={
        "nombre_materia": "Álgebra Lineal",
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["Materia"]
    assert data["nombre_materia"] == "Álgebra Lineal"


def test_eliminar_materia(client):
    crearProfe(client,2,"Juanes","Montoya")
    crearMateria(client,4,"Ciencias Sociales",2)
    response = client.delete("/materia/4")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Materia eliminada"

# Test errores

def test_obtener_materias_vacio(client):
    response = client.get("/materias")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No se encontraron materias"

def test_obtener_materia_por_id_vacio(client):
    response = client.get("/materia/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Materia no encontrada"

def test_actualizar_materia_inexistente(client):
    response = client.put("/materia/2", json={
        "nombre_materia": "Álgebra Lineal",
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Materia no encontrada"

def test_eliminar_materia_inexistente(client):
    response = client.delete("/materia/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Materia no encontrada"