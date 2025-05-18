import pytest
from fastapi.testclient import TestClient
from starlette import status
from app.database import (
    Alumno,
    Alumno_Materia,
    Materia,
    set_database,
    db_prueba,
    myDB,
)
from app.test.test_alumnos_materias import crearAlumno
from app.main import app


@pytest.fixture(scope="function", autouse=True)
def client():
    set_database(db_prueba)  # Se cambia a la BD de testeo
    if db_prueba.is_closed():
        db_prueba.connect()
    db_prueba.create_tables([Alumno, Alumno_Materia, Materia])
    with TestClient(app) as c:
        yield c
    db_prueba.drop_tables([Alumno, Alumno_Materia, Materia])
    db_prueba.close()
    set_database(myDB)  # Se restaura a la BD original


# Test CRUD


def test_crear_alumno(client):
    response = client.post(
        "/alumno",
        json={
            "id_alumno": 1,
            "nombre_alumno": "Juan",
            "apellido_alumno": "Pérez",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()["__data__"]
    assert data["id_alumno"] == 1
    assert data["nombre_alumno"] == "Juan"
    assert data["apellido_alumno"] == "Pérez"


def test_obtener_todos_alumnos(client):
    crearAlumno(client, 1, "Juan", "Pérez")
    crearAlumno(client, 2, "Ana", "Gómez")
    response = client.get("/alumnos")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id_alumno"] == 1
    assert data[1]["nombre_alumno"] == "Ana"


def test_obtener_alumno_por_id(client):
    crearAlumno(client, 2, "Ana", "Gómez")
    response = client.get("/alumno/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["__data__"]
    assert data["id_alumno"] == 2
    assert data["nombre_alumno"] == "Ana"


def test_actualizar_alumno(client):
    crearAlumno(client, 3, "Carlos", "Sosa")
    response = client.put(
        "/alumno/3",
        json={"nombre_alumno": "Carlos A.", "apellido_alumno": "Sosa B."},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["alumno"]
    assert data["nombre_alumno"] == "Carlos A."
    assert data["apellido_alumno"] == "Sosa B."


def test_eliminar_alumno(client):
    crearAlumno(client, 4, "Laura", "Rodríguez")
    response = client.delete("/alumno/4")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Alumno eliminado"


# Test errores


def test_obtener_alumnos_vacio(client):
    response = client.get("/alumnos")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No se encontraron alumnos"


def test_obtener_alumno_por_id_vacio(client):
    response = client.get("/alumno/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Alumno no encontrado"


def test_actualizar_alumno_inexistente(client):
    response = client.put(
        "/alumno/1",
        json={"nombre_alumno": "Juan", "apellido_alumno": "Roberto"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Alumno no encontrado"


def test_eliminar_alumno_inexistente(client):
    response = client.delete("/alumno/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Alumno no encontrado"
