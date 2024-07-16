import flet as ft

from library.core.widgets.text import Text


class Title(Text):
    def __init__(self, text):
        super().__init__(
            value=text,
            size=24,
            weight=ft.FontWeight.W_500
        )


def set_page(routes, selected_index):
    FormData = routes[selected_index]["page"]
    title = Title(routes[selected_index]["title"])
    page = [FormData]

    if title.value:
        page = [title, FormData]

    if isinstance(FormData, ft.UserControl):
        return ft.Column(page, expand=True)
    return ft.ListView(page, expand=True)


class CustomNavigation(ft.UserControl):
    def __init__(
        self,
        *,
        routes: list = [],
        selected_index: int = 0,
    ):
        super().__init__()
        self.expand = True
        self.routes = routes
        self.selected_index = selected_index

        self.destinations = list(map(self.get_destinations, routes))

    def get_destinations(self, icons):
        return ft.NavigationRailDestination(
            icon=icons["icon"][0],
            selected_icon=icons["icon"][1],
        )

    def navigation(self, index: str):
        self.row.controls[2] = set_page(self.routes, index)
        self.update()

    def build(self):
        self.state = set_page(self.routes, self.selected_index)

        self.rail = ft.NavigationRail(
            selected_index=self.selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=True,
            width=70,
            destinations=self.destinations,
            on_change=lambda e: self.navigation(e.control.selected_index),
            bgcolor=ft.colors.WHITE,
        )
        self.row = ft.Row(
            controls=[
                self.rail,
                ft.VerticalDivider(width=1),
                self.state
            ],
        )
        return self.row
