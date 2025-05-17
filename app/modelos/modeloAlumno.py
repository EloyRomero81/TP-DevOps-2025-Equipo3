from pydantic import BaseModel

# Se definen los modelos para validar los datos que se esperan


class ModeloCrearAlumno(BaseModel):
    id_alumno: int
    nombre_alumno: str
    apellido_alumno: str


class ModeloActualizarAlumno(BaseModel):
    nombre_alumno: str
    apellido_alumno: str
