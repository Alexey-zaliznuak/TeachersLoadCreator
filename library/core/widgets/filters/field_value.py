from typing import Any
import flet as ft
from .filter_field import FilterField
from peewee import ForeignKeyField


LABEL_ID = 0
KEY_ID = 1


class FilterValueFieldWidget(ft.UserControl, FilterField):
    def __init__(self, field, form, datatable):
        self.field = field
        self.form = form
        self.datatable = datatable
        self.checkboxes: list[ft.Checkbox] = self._build_checkboxes()
        super().__init__()

    def build(self):
        # todo upgrade ui
        return ft.Column(self.checkboxes)

    def _build_checkboxes(self):
        checkboxes = []
        checkboxes_params: list[tuple[str, Any]] = []

        for obj in self.form.Meta.model.select():
            field_value = getattr(obj, self.field.name)

            if isinstance(self.field, ForeignKeyField):
                label = str(field_value)
                field_value = getattr(obj, self.field.name + '_id')
            else:
                label = field_value

            checkboxes_params.append((label, field_value))

        checkboxes_params = set(checkboxes_params)

        for param in checkboxes_params:
            checkboxes.append(
                ft.Checkbox(
                    label=param[LABEL_ID], key=param[KEY_ID], value=True
                )
            )

        return checkboxes

    @property
    def value(self):
        values = []

        for chb in self.checkboxes:
            if chb.value:
                values.append(chb.key)

        return values
