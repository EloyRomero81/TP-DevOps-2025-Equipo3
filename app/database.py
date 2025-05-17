from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    CharField,
    ForeignKeyField,
    CompositeKey,
)


myDB = SqliteDatabase(
    "app/database.sqlite", pragmas={"foreign_keys": 1}
)  # Se indica la BD con la que se trabajará y se enforza
   # las restricciones de claves foráneas.
db_prueba = SqliteDatabase(
    "file:memdb1?mode=memory&cache=shared",
    uri=True,
    pragmas={"foreign_keys": 1},
    check_same_thread=False,
)  # Para testeo


class BaseModel(Model):
    class Meta:
        database = myDB


# Función para cambiar la base de datos (para testeo)
def set_database(new_db):
    for model in [Alumno, Alumno_Materia, Materia, Profesor]:
        model._meta.database = new_db


# Se define la estructura que tiene la BD
class Alumno(BaseModel):
    id_alumno = IntegerField(primary_key=True)
    nombre_alumno = CharField(max_length=50)
    apellido_alumno = CharField(max_length=50)


class Profesor(BaseModel):
    id_profesor = IntegerField(primary_key=True)
    nombre_profesor = CharField(max_length=50)
    apellido_profesor = CharField(max_length=50)


class Materia(BaseModel):
    id_materia = IntegerField(primary_key=True)
    nombre_materia = CharField(max_length=50)
    id_profesor = ForeignKeyField(
        Profesor, backref="materia", column_name="id_profesor"
    )  # backref crea un acceso inverso desde Profesor hacia Materia.
    # Peewee por defecto genera el nombre del campo como id_profesor_id en la base de datos,
    # no como id_profesor. Por eso se lo cambia con column_name.


class Alumno_Materia(BaseModel):
    id_alumno = ForeignKeyField(
        Alumno, backref="notas", column_name="id_alumno"
    )
    id_materia = ForeignKeyField(
        Materia, backref="notas", column_name="id_materia"
    )
    nota_parcial1 = IntegerField(null=True)
    nota_parcial2 = IntegerField(null=True)
    nota_final = IntegerField(null=True)

    class Meta:
        primary_key = CompositeKey("id_alumno", "id_materia")
