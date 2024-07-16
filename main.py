import flet as ft

from models import init_tables
from widgets.Executor import Executor

# from widgets.CustomNavigation import CustomNavigation


init_tables()

from filtersets import NicknamesFilterSet
from forms import NicknamesForm, PersonsForm


def main(page: ft.Page):
    # TODO global context class
    page.theme_mode = ft.ThemeMode.LIGHT
    page.datatables = []
    page.title = 'Fletty birds'

    t = ft.Tabs(
        selected_index=2,
        animation_duration=50,
        tabs=[
            ft.Tab(
                text="Преподы",
                content=ft.ListView(
                    [PersonsForm().DataTable()[0]],
                    padding=ft.Padding(0, 10, 0, 0)
                )
            ),
            ft.Tab(
                text="Псевдонимы",
                content=ft.ListView(
                    [NicknamesForm().DataTable(filterset=NicknamesFilterSet)[0]],
                    padding=ft.Padding(0, 10, 0, 0)
                )
            ),
            ft.Tab(
                text="Выполнение",
                content=ft.ListView(
                    [Executor()],
                    padding=ft.Padding(0, 10, 0, 0)
                ),
            )
        ],
        expand=True
    )

    page.add(
        ft.Row(
            controls=[t],
            expand=True,
        )
    )


ft.app(target=main)
