from pydantic import BaseModel
from typing import Optional

# Se definen los modelos para validar los datos que se esperan


class ModeloCrearAlumnoMateria(BaseModel):
    id_alumno: int
    id_materia: int
    nota_parcial1: Optional[int] = None
    nota_parcial2: Optional[int] = None
    nota_final: Optional[int] = None


class ModeloActualizarAlumnoMateria(
    BaseModel
):  # Se pueden actualizar todas las notas o solo algunas
    nota_parcial1: Optional[int] = None
    nota_parcial2: Optional[int] = None
    nota_final: Optional[int] = None
