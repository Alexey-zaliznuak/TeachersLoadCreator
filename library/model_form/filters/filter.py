import flet as ft

import flet as ft
from library.core.widgets.filters import FilterField


class Filter:
    widget_: FilterField = ...

    def __init__(self, *args, **kwargs):
        self.filter_widget: ft.Control = None

    def widget(self, form, datatable) -> ft.Control:
        self.filter_widget = self.widget_(form, datatable)
        return self.filter_widget

    def filter(self, queryset):
        ...
