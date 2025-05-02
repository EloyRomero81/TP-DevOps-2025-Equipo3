from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Dirección de nuestra base de datos (usamos SQLite para que sea simple)
URL_BD = "sqlite:///./prueba.db"

# Esto es como abrir la puerta a la base de datos
motor = create_engine(URL_BD, connect_args={"check_same_thread": False})

# Esta "herramienta" nos deja pedir acceso a la base de datos (una sesión)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)
