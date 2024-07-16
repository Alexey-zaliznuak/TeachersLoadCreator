import flet as ft
import re

from .BaseViewer import Viewer
from .BaseInput import InputField
from library.core.widgets.text import Text


class PhoneParent:
    MASK = '+7 (XXX) XXX-XX-XX'

    def input_mask(self, value):
        result = self.MASK
        text = ''.join(i for i in value if i.isdigit())

        for char in text:
            result = result.replace('X', char, 1)

        result = result.replace('X', "?")
        return result


class PhoneViewer(Text, PhoneParent, Viewer):
    def __init__(self, value: str):
        super().__init__(
            value=self.input_mask(value),
            width=150,
            style=ft.ButtonStyle(
                color=ft.colors.BLACK87
            ),
        )


class PhoneInput(ft.TextField, PhoneParent, InputField):

    MASK = '(XXX) XXX-XX-XX'

    def __init__(self, default_value: str):
        super().__init__(
            value=self.input_mask(default_value),
            icon=ft.icons.PHONE,
            hint_text='(123) 456-78-90',
            prefix_text='+7 ',
            label="Your phone number",
            keyboard_type=ft.KeyboardType.PHONE,
            on_change=self.broker_input,
        )

    @property
    def clear_value(self):
        return ''.join(i for i in self.value if i.isdigit())

    def broker_input(self, e):
        mask = self.MASK
        text = ''.join(i for i in e.control.value if i.isdigit())

        for char in text:
            mask = mask.replace('X', char, 1)

        r = re.compile(r'[^\d]+')

        result = mask
        if mask.find('X') != -1:
            result = mask.replace(re.findall(r, mask)[-1], '', 1)

        self.value = result
        self.update()
