from pydantic import BaseModel

#Se definen los modelos para validar los datos que se esperan

class ModeloCrearProfesor(BaseModel):
    id_profesor: int
    nombre_profesor: str
    apellido_profesor: str

# Lo que se devuelve cuando se MUESTRA un estudiante
class ModeloActualizarProfesor(BaseModel):
    nombre_profesor: str
    apellido_profesor: str