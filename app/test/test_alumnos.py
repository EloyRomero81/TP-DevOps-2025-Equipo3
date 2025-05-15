import pytest
from fastapi.testclient import TestClient
from app.database import Alumno, Alumno_Materia, Materia, set_database, db_prueba, myDB
from app.main import app

@pytest.fixture(scope="function", autouse=True)
def client():        
    set_database(db_prueba)  #Se cambia a la BD de testeo
    if db_prueba.is_closed():
        db_prueba.connect()    
    db_prueba.create_tables([Alumno, Alumno_Materia, Materia])
    with TestClient(app) as c:
        yield c
    db_prueba.drop_tables([Alumno, Alumno_Materia, Materia])
    db_prueba.close()
    set_database(myDB) #Se restaura a la BD original

def test_crear_alumno(client):
    response = client.post("/alumno", json={
        "id_alumno": 1,
        "nombre_alumno": "Juan",
        "apellido_alumno": "Pérez"
    })
    assert response.status_code == 200
    data = response.json()["__data__"]
    assert data["id_alumno"] == 1
    assert data["nombre_alumno"] == "Juan"
    assert data["apellido_alumno"] == "Pérez"

def test_obtener_alumnos_vacio(client):
    response = client.get("/alumnos")
    assert response.status_code == 404
    assert response.json()["detail"] == "No se encontraron alumnos"

def test_obtener_alumno_por_id(client):
    client.post("/alumno", json={
        "id_alumno": 2,
        "nombre_alumno": "Ana",
        "apellido_alumno": "Gómez"
    })
    response = client.get("/alumno/2")
    print("RESPONSE JSON:", response.json())
    assert response.status_code == 200
    data = response.json()["__data__"]
    assert data["id_alumno"] == 2
    assert data["nombre_alumno"] == "Ana"

def test_actualizar_alumno(client):
    client.post("/alumno", json={
        "id_alumno": 3,
        "nombre_alumno": "Carlos",
        "apellido_alumno": "Sosa"
    })
    response = client.put("/alumno/3", json={
        "nombre_alumno": "Carlos A.",
        "apellido_alumno": "Sosa B."
    })
    assert response.status_code == 200
    data = response.json()["alumno"]
    assert data["nombre_alumno"] == "Carlos A."
    assert data["apellido_alumno"] == "Sosa B."

def test_eliminar_alumno(client):
    client.post("/alumno", json={
        "id_alumno": 4,
        "nombre_alumno": "Laura",
        "apellido_alumno": "Rodríguez"
    })
    response = client.delete("/alumno/4")
    assert response.status_code == 200
    assert response.json() == "Alumno eliminado"