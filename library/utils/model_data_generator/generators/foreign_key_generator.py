from .field_generator import FieldGenerator
from functools import cached_property
from random import choice
from peewee import Model


class ForeignKeyGenerator(FieldGenerator):
    def __init__(
        self,
        model: Model,
        *,
        to_field: str = 'id'
    ):
        self.model = model
        self.to_field = to_field

    def __call__(self) -> int:
        choices = list(map(
            lambda el: getattr(el, self.to_field), self.queryset
        ))

        assert choices, f'No {self.model} objects for choices.'
        return choice(choices)

    @cached_property
    def queryset(self):
        return self.model.select()
