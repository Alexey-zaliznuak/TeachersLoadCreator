from faker import Faker
from typing import Sequence

from .field_generator import FieldGenerator


class TextGenerator(FieldGenerator):
    # What did you expect? Api to the "ChatGPT"?

    def __init__(
        self,
        max_nb_chars: int = 200,
        ext_word_list: Sequence[str] = None,
        *,
        locate=None
    ):
        self.faker = Faker(locate)

        self.max_nb_chars = max_nb_chars
        self.ext_word_list = ext_word_list

    def __call__(self) -> str:
        return self.faker.text(self.max_nb_chars, self.ext_word_list)
