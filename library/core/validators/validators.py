import peewee
import validators
from typing import Any
from library.core.exceptions import ValidationError


class ValueValidator:
    def __init__(self, mn: int = None, mx: int = None) -> None:
        if not (mn or mx):
            raise AttributeError('Макс. или мин. должно быть определено')
        if mx and mn and mx < mn:
            raise ValueError('Макс. должно быть больше мин.')

        self.mx = mx
        self.mn = mn

    def __call__(self, value):
        if self.mx and value > self.mx:
            raise ValidationError(
                f'Длинна не может быть больше {self.mx}'
            )

        if self.mn and value < self.mn:
            raise ValidationError(
                f'Длинна должна быть более {self.mn}'
            )


class LengthValidator(ValueValidator):
    def __call__(self, value):
        errors = []

        if value is None:
            value = 0
        else:
            value = len(value)

        if self.mx and value > self.mx:
            raise ValidationError(
                f'Длинна не может быть больше {self.mx}'
            )

        if self.mn and value < self.mn:
            raise ValidationError(
                f'Длинна должна быть более {self.mn}'
            )

        return errors


class URLValidator():
    def __call__(self, value) -> Any:
        try:
            validators.url(value)
        except validators.ValidationError:
            raise ValidationError('Неверный формат URL')


class PhoneValidator():
    NUMBERS_IN_PHONE_COUNT = 10

    def __call__(self, value: str) -> Any:
        c = 0
        for s in value:
            if s.isdigit():
                c += 1

        if c != self.NUMBERS_IN_PHONE_COUNT:
            raise ValidationError(f'Невалидный формат номера - {c+1}')


class ForeignKeyValidator():
    def __init__(self, model_to: peewee.Model) -> None:
        self.model_to = model_to

    def __call__(self, pk):
        try:
            self.model_to.get_by_id(pk)
        except peewee.DoesNotExist:
            raise ValidationError(
                'Объект с таким идентификатором не существует'
            )


class DaysFieldDefaultValidator:
    COUNT_DAYS_SEPARATOR = ':'
    DAYS_SEPARATOR = ';'

    def __call__(self, value: str):
        if not (1 <= value[0] <= 7):
            raise ValidationError(f'Некорректное количество дней - {value}')

        count, days = value.split(self.COUNT_DAYS_SEPARATOR)

        if len(days.split(self.DAYS_SEPARATOR)) != int(count):
            raise ValidationError('Некорректное количество выбранных дней')
