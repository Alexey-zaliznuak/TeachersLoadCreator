from faker import Faker

from .field_generator import FieldGenerator


class NameGenerator(FieldGenerator):
    def __init__(
        self,
        first_name: bool = True,
        last_name: bool = True,
        *,
        locate: str = 'en_US'
    ):

        assert first_name or last_name, (
            'At least one of first or last names must be specified.'
        )

        self.faker = Faker(locate)
        self.first_name = first_name
        self.last_name = last_name

    def __call__(self) -> str:
        # TODO patronymic
        names = []

        if self.first_name:
            names.append(self.faker.first_name())

        if self.last_name:
            names.append(self.faker.last_name())

        return ' '.join(names)
