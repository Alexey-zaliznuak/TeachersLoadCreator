from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, CrossAxisAlignment, MainAxisAlignment, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue, ScrollMode

from library.core.widgets.fields.BaseInput import InputField
from library.core.widgets.fields.BaseViewer import Viewer


class DayButton(ft.ElevatedButton):
    def __init__(
            self,
            text,
            select=False,
            weekend=False,
            check=lambda: ...
    ):
        self.select = select
        self.weekend = weekend
        self.check = check
        self.style = self.change_style()

        super().__init__(
            style=self.style,
            text=text,
            on_click=self.change_select_click
        )

    def change_style(self):
        style = ft.ButtonStyle(
            bgcolor={
                "": None if not self.select else ft.colors.BLUE_400
            },
            color={
                "": ft.colors.BLACK
            }
        )

        if self.weekend:
            style = ft.ButtonStyle(
                bgcolor={
                    "": None if not self.select else ft.colors.YELLOW_800
                },
                color={
                    "": ft.colors.BLACK
                }
            )
        return style

    def change_select_click(self, e):
        i_adding = not self.select
        if self.check(i_adding):
            self.select = not self.select
            e.control.style = self.change_style()
        e.control.update()


class DaysField(ft.UserControl):
    def __init__(
        self,
        value: str,
        check=lambda: ...
    ):
        cnt_vlu = '0:'
        if value:
            cnt_vlu = value.split(':')
        self.count = cnt_vlu[0]
        self.value = cnt_vlu[1].split(';')
        self.check = check

        days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        weekends = ['ВС']

        self.buttons = list(
            map(
                lambda day: DayButton(
                    text=day.upper(),
                    check=self.check_all,
                    weekend=day in weekends
                ),
                days
            )
        )

        super().__init__()

    def check_all(self, add):
        count = len([button for button in self.buttons if button.select])
        if add:
            return count < self.check()
        else:
            return True

    @property
    def clear_value(self):
        return {
            'buttons': [
                button.text.lower()
                for button in self.buttons if button.select
            ],
            'count': self.check()
        }

    def build(self):
        return ft.Row(
            [
                ft.Column([
                    ft.Row([
                        *self.buttons[0:3]
                    ]),
                    ft.Row([
                        *self.buttons[3:6]
                    ]),
                    ft.Container(
                        self.buttons[6],
                        margin=ft.margin.only(0, 10, 0, 0)
                    ),
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),

            ]
        )


class GetMaximum(ft.Row):
    def __init__(self, value=1):
        self.value = value

        txt_number = ft.Text(
            value=str(value),
            text_align="right",
            width=10
        )

        super().__init__(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=self.minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=self.plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def minus_click(self, e):
        self.value = int(self.controls[1].value) - 1
        if self.value < 1:
            self.value = 1
        self.controls[1].value = str(self.value)
        self.update()

    def plus_click(self, e):
        self.value = int(self.controls[1].value) + 1

        if self.value > 3:
            self.value = 3

        self.controls[1].value = str(self.value)
        self.update()

    @property
    def clear_value(self):
        return self.value


class DaysAndCounterPicker(ft.UserControl, InputField):
    def __init__(
        self,
        value: str
    ):
        self.WeekField = DaysField(check=self.check_if_maximum, value=value)
        self.GetMaximum = GetMaximum()

        super().__init__()

    def check_if_maximum(self):
        return self.GetMaximum.clear_value

    def build(self):
        return ft.Column(
            [
                self.GetMaximum,
                self.WeekField,
            ],
            width=220
        )

    @property
    def clear_value(self):
        ret = self.WeekField.clear_value
        print(ret)
        days = ';'.join(ret['buttons'])
        count = ret['count']
        return f'{count}:{days}'

class DaysViewer(ft.Row, Viewer):
    def __init__(self, value=''):

        
        cnt_vlu = value.split(':') if value else '0:'
        self.value = cnt_vlu[1].split(';')

        super().__init__(
            [
                ft.ElevatedButton(
                    text=text.upper()
                ) for text in self.value
            ]
        )