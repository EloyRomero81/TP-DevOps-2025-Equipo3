from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Esto es el molde para la base de datos
class EstudianteBD(Base):
    __tablename__ = 'estudiantes'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)

# Esto es el molde para cuando alguien quiere enviar o recibir datos por la API

# Lo que se espera al CREAR un estudiante
class CrearEstudiante(BaseModel):
    nombre: str
    correo: str

# Lo que se devuelve cuando se MUESTRA un estudiante
class Estudiante(CrearEstudiante):
    id: int

    class Config:
        orm_mode = True  # Le dice a FastAPI que esto viene de la base de datos