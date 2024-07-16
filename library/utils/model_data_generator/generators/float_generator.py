from .field_generator import FieldGenerator
from functools import partial
from random import randint, random


class FloatGenerator(FieldGenerator):
    def __init__(
        self,
        mn: int = -10**9,
        mx: int = 10**9,
        *,
        only_positive: bool = False
    ):
        self.mn = mn
        self.mx = mx

        if only_positive:
            self.mn = max(0, mn)

        assert mn < mx, "Invalid value: min value is greater than max."

    def __call__(self) -> int:
        return randint(self.mn, self.mx) + random()


PositiveFloatGenerator = partial(FloatGenerator, only_positive=True)
