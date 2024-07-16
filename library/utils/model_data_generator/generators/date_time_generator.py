from datetime import datetime
from functools import partial
from typing import Callable
from random import randint

from .field_generator import FieldGenerator


# TODO all from
# docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

class DateTimeFormatGenerator(FieldGenerator):
    def __init__(self, template: str):
        self.mapping: dict[str, Callable] = {
            "%d": self.int_day,
            "%m": partial(self.int_month, with_zeros=True),
            "%Y": partial(self.int_year, with_zeros=True),
            "%H": partial(self.int_hour, with_zeros=True),
            "%M": partial(self.int_minute, with_zeros=True),
            "%S": partial(self.int_second, with_zeros=True),
        }

        self.origin_template = template

    def __call__(self):
        template = self.origin_template

        for key, func in self.mapping.items():
            while key in template:
                template = template.replace(key, str(func()), 1)

        return template

    def int_day(self, with_zeros: bool = True):
        day = randint(1, 30)

        if day < 10 and with_zeros:
            day = '0' + str(day)

        return day

    def int_month(self, with_zeros: bool = True):
        month = randint(1, 12)
        if month < 10 and with_zeros:
            month = '0' + str(month)

        return month

    def int_year(
        self,
        mn: int = datetime.now().year - 100,
        mx: int = datetime.now().year,
        with_zeros: bool = True
    ):
        assert mn <= mx, f'invalid minimum and maximum years: {mn}, {mx}'

        year = randint(mn, mx)

        if with_zeros:
            year = f"{year:04d}"

        return year

    def int_hour(self, with_zeros: bool = True):
        hour = randint(0, 23)

        if with_zeros:
            hour = f"{hour:02d}"

        return hour

    def int_minute(self, with_zeros: bool = True):
        minute = randint(0, 23)

        if with_zeros:
            minute = f"{minute:02d}"

        return minute

    def int_second(self, with_zeros: bool = True):
        second = randint(0, 23)

        if with_zeros:
            second = f"{second:02d}"

        return second


DateGenerator = partial(
    DateTimeFormatGenerator, '%Y-%m-%d'
)
TimeGenerator = partial(
    DateTimeFormatGenerator, '%H:%M:%S'
)
DateTimeGenerator = partial(
    DateTimeFormatGenerator, '%Y-%m-%d %H:%M:%S'
)
