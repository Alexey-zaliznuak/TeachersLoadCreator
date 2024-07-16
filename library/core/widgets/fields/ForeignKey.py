import flet as ft
from .BaseViewer import Viewer
from library.core.widgets.actions.objects.detail import (
    DetailObjectActionDialog
)
from .BaseInput import InputField


class ForeignKeyViewer(ft.Container, Viewer):
    has_value_for_copy = False

    def __init__(
        self,
        obj,
        fields,
        label: str,
    ):
        self.obj = obj
        self.fields = fields

        if len(label) > 25:
            label = label[:22] + "..."

        super().__init__(
            content=ft.TextButton(text=label, on_click=self.open_detail_modal),
        )

    def open_detail_modal(self, e=None):
        # TODO While open https://github.com/flet-dev/flet/issues/1670
        # don`t open NEW modal
        if not getattr(self.page.dialog, 'open', False):
            # self.page.dialog.open = False
            self.page.dialog = DetailObjectActionDialog(self.obj, self.fields)
            self.page.dialog.open = True
            self.page.update()


class ForeignKeyEditor(ft.Dropdown, InputField):
    defaults = {
        'width': 300,
        'hint_text': 'Выберете',
    }

    def __init__(self, queryset, default_key=None):  # TODO filters
        return super().__init__(
            options=[
                ft.dropdown.Option(text=str(obj), key=obj.id)
                for obj in queryset()
            ],
            value=default_key,
            **self.defaults
        )
