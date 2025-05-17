from pydantic import BaseModel
from typing import Optional

# Se definen los modelos para validar los datos que se esperan


class ModeloCrearMateria(BaseModel):
    id_materia: int
    nombre_materia: str
    id_profesor: int


class ModeloActualizarMateria(BaseModel):
    nombre_materia: Optional[str] = None
    id_profesor: Optional[int] = None
