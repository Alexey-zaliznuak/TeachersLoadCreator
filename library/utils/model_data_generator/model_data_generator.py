from functools import lru_cache
from typing import Callable, Iterable, Optional

import peewee
from peewee import Field as DataBaseField
from peewee import Model

from .generators import (
    BooleanGenerator,
    DateGenerator,
    DateTimeGenerator,
    FloatGenerator,
    IntegerGenerator,
    TextGenerator,
    TimeGenerator,
    UUIDGenerator,
)


class ModelDataGenerator():
    "Create random data for your model."

    generated_objects: list[dict] = []
    fields_mapping: dict[DataBaseField, Callable] = {
        peewee.DateField: DateGenerator,
        peewee.DateTimeField: DateTimeGenerator,
        peewee.FloatField: FloatGenerator,
        peewee.BooleanField: BooleanGenerator,
        peewee.IntegerField: IntegerGenerator,
        peewee.TextField: TextGenerator,
        peewee.TimeField: TimeGenerator,
        peewee.UUIDField: UUIDGenerator,
    }

    @classmethod
    def generate_rows(cls, count: int) -> list[dict]:
        objects = []

        for _ in range(count):
            obj = {}

            for field, mthd in cls.__fields().items():
                obj[field] = mthd()

            objects.append(obj)

        cls.generated_objects = objects
        return objects

    @classmethod
    def save(cls):
        assert cls.generated_objects, 'Not rows for saving. Use generate_rows'
        cls.Meta.model.insert_many(cls.generated_objects).execute()

    @classmethod
    @lru_cache(maxsize=None)
    def __fields(cls) -> dict[str, Callable]:
        # TODO ClassLookupDict
        fields = {}

        for field in cls.Meta.fields:
            custom_field = getattr(cls, field, None)

            if custom_field:
                fields[field] = custom_field
            else:
                fields[field] = cls.fields_mapping[
                    getattr(cls.Meta.model, field).__class__
                ]()

        return fields

    class Meta:
        model: Optional[Model] = None
        fields: Iterable[str] = ()
