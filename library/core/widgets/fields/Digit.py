import flet as ft

from library.core.widgets.text import Text

from .BaseViewer import Viewer
from .BaseInput import InputField


class IntegerInput(ft.Row, InputField):

    def __init__(
        self,
        value: int,
    ):
        txt_number = ft.TextField(
            value=str(value),
            text_align="right",
            width=100
        )

        super().__init__(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=self.minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=self.plus_click),
            ]
        )

    def minus_click(self, e):
        self.controls[1].value = str(int(self.controls[1].value) - 1)
        self.update()

    def plus_click(self, e):
        self.controls[1].value = str(int(self.controls[1].value) + 1)
        self.update()

    @property
    def clear_value(self):
        cleared = ''.join(s for s in self.controls[1].value if s.isdigit())
        if cleared:
            return int(cleared)
        return ''


class FloatViewer(Text, Viewer):
    def __init__(
        self,
        value: float,
    ):
        number = str(value).split('.')
        if len(number) < 2:
            number.append('00')

        self.dot = ft.TextSpan(
            text='.',
            style=ft.TextStyle(size=18),
        )
        self.text_float = ft.TextSpan(
            text=str(number[1]),
            style=ft.TextStyle(size=18),
        )
        super().__init__(
            value=str(number[0]),
            size=24,
            selectable=True,
            spans=[
                self.dot,
                (self.text_float if number[1]
                 else None),
            ]
        )


class IntegerViewer(Text, Viewer):
    "View content as Text."
    pass
