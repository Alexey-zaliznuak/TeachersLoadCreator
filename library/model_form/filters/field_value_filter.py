from typing import Iterable

import flet as ft
from .filter import Filter
from library.core.widgets.filters import FilterValueFieldWidget
from library.types import AllPossibleValues


class FieldValueFilter(Filter):
    widget_ = FilterValueFieldWidget

    def __init__(self, field, value=AllPossibleValues):
        self.field = field
        self.value = value
        self.filter_widget = None

    def filter(self, queryset: Iterable):
        values = [self.value]

        if self.filter_widget:
            filter_value = self.filter_widget.value
            if not filter_value and self.value is AllPossibleValues:
                return []

            if isinstance(filter_value, list):
                values.extend(filter_value)
            else:
                values.append(filter_value)

        if len(values) == values.count(AllPossibleValues):
            return queryset

        values = set(values)
        if AllPossibleValues in values:
            values.remove(AllPossibleValues)

        return queryset.where(self.field.in_(values))

    def widget(self, form, datatable) -> ft.Control:
        if not self.filter_widget:
            self.filter_widget = self.widget_(self.field, form, datatable)

        return self.filter_widget
