import pytest
from fastapi.testclient import TestClient
from starlette import status
from app.database import Profesor, set_database, db_prueba, myDB
from app.main import app

@pytest.fixture(scope="function", autouse=True)
def client():        
    set_database(db_prueba)  #Se cambia a la BD de testeo
    if db_prueba.is_closed():
        db_prueba.connect()    
    db_prueba.create_tables([Profesor])
    with TestClient(app) as c:
        yield c
    db_prueba.drop_tables([Profesor])
    db_prueba.close()
    set_database(myDB) #Se restaura a la BD original

#Test CRUD

def test_crear_profesor(client):
    response = client.post("/profesor", json={
        "id_profesor": 1,
        "nombre_profesor": "Alberto",
        "apellido_profesor": "Vilda"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()["__data__"]
    assert data["id_profesor"] == 1
    assert data["nombre_profesor"] == "Alberto"
    assert data["apellido_profesor"] == "Vilda"

def test_obtener_todos_profesores(client):
    client.post("/profesor", json={
        "id_profesor": 1,
        "nombre_profesor": "Alberto",
        "apellido_profesor": "Vilda"
    })
    client.post("/profesor", json={
        "id_profesor": 2,
        "nombre_profesor": "Enrique",
        "apellido_profesor": "Castillos"
    })
    response = client.get("/profesores")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id_profesor"] == 1
    assert data[1]["nombre_profesor"] == "Enrique"
    

def test_obtener_profesor_por_id(client):
    client.post("/profesor", json={
        "id_profesor": 2,
        "nombre_profesor": "Enrique",
        "apellido_profesor": "Castillos"
    })
    response = client.get("/profesor/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["__data__"]
    assert data["id_profesor"] == 2
    assert data["nombre_profesor"] == "Enrique"

def test_actualizar_profesor(client):
    client.post("/profesor", json={
        "id_profesor": 3,
        "nombre_profesor": "Carlos",
        "apellido_profesor": "Sosa"
    })
    response = client.put("/profesor/3", json={
        "nombre_profesor": "Marcelo",
        "apellido_profesor": "Dominguez"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["profesor"]
    assert data["nombre_profesor"] == "Marcelo"
    assert data["apellido_profesor"] == "Dominguez"

def test_eliminar_profesor(client):
    client.post("/profesor", json={
        "id_profesor": 4,
        "nombre_profesor": "Marcela",
        "apellido_profesor": "Trailla"
    })
    response = client.delete("/profesor/4")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Profesor eliminado"

# Test errores

def test_obtener_profesores_vacio(client):
    response = client.get("/profesores")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No se encontraron profesores"

def test_obtener_profesor_por_id_vacio(client):
    response = client.get("/profesor/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Profesor no encontrado"

def test_actualizar_profesor_inexistente(client):
    response = client.put("/profesor/1", json={
        "nombre_profesor": "Juan",
        "apellido_profesor": "Roberto"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Profesor no encontrado"

def test_eliminar_profesor_inexistente(client):
    response = client.delete("/profesor/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Profesor no encontrado"
    