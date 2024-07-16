import flet as ft
from .BaseViewer import Viewer
from .BaseInput import InputField


class BooleanViewer(ft.Checkbox, Viewer):
    has_value_for_copy = False

    def __init__(
        self,
        value,
        tristate: bool = False,
        label_position: ft.LabelPosition = ft.LabelPosition.RIGHT,
        label: str = '',

    ):
        super().__init__(
            value=bool(value),
            tristate=tristate,
            disabled=True,
            label_position=label_position,
            label=label,
        )


class BooleanInput(ft.Checkbox, InputField):
    has_value_for_copy = False

    def __init__(
        self,
        value: bool,
        tristate: bool = False,
        label_position: ft.LabelPosition = ft.LabelPosition.RIGHT,
        label: str = '',
    ):
        super().__init__(
            value=bool(value),
            tristate=tristate,
            label_position=label_position,
            label=label,
        )
