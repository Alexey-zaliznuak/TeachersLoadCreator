from uuid import uuid4

from .field_generator import FieldGenerator


class UUIDGenerator(FieldGenerator):
    def __call__(self):
        return uuid4()
