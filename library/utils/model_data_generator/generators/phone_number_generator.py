from faker import Faker

from .field_generator import FieldGenerator


class PhoneNumberGenerator(FieldGenerator):
    phones_templates: dict[str, str] = {
        'RUSSIA': '+7 (###) ###-##-##',
    }

    def __init__(
        self,
        country: str = 'RUSSIA'
    ):
        # TODO random country / many countries
        self.template = self.phones_templates[country.upper()]
        self.faker = Faker()

    def __call__(self) -> str:
        return self.faker.bothify(self.template)
