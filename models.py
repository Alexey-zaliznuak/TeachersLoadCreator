import os
import sys
from peewee import (
    CharField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
)
from library.core.exceptions import ValidationError


# pragmas is sqlite mega move
db = SqliteDatabase("db.db", pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField(max_length=100, help_text='ФИО препода')

    def __str__(self) -> str:
        return self.name

    def validate(obj, create=False, id_=None):
        if create and (
            Nickname.select().where(Nickname.name==obj['name']).exists()
            or Person.select().where(Person.name==obj['name']).exists()
        ):
            raise ValidationError('Препод или псевдоним с таким именем уже существует!')

        return obj



class Nickname(BaseModel):
    name = CharField(max_length=100, help_text='Псевдоним')
    person = ForeignKeyField(
        Person,
        to_field='id',
        on_delete='CASCADE',
        help_text='Препод'
    )

    def validate(obj, create=False, id_=None):
        if create and (
            Nickname.select().where(Nickname.name==obj['name']).exists()
            or Person.select().where(Person.name==obj['name']).exists()
        ):
            raise ValidationError('Препод или псевдоним с таким именем уже существует!')

        return obj

    def __str__(self) -> str:
        return self.name


def init_tables():
    tables = [
        Person,
        Nickname,
    ]

    def remake_db():
        print('create')
        try:
            db.connect()
        except Exception:
            pass
        db.drop_tables(tables)
        db.create_tables(tables)

    if '--make' in sys.argv:
        remake_db()
        return

    if os.path.exists('./db.db'):
        try:
            db.connect()
        except Exception:
            pass
        if __name__ == '__main__':
            db.drop_tables(tables)
        db.create_tables(tables)
    else:
        remake_db()


if __name__ == '__main__':
    pass
    init_tables()
