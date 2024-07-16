from .field_generator import FieldGenerator
from random import getrandbits


class BooleanGenerator(FieldGenerator):
    def __call__(self) -> bool:
        return bool(getrandbits(1))
