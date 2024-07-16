import flet as ft
from library.core.widgets.text import Text, TitleText

from excel_formatter import main as make, get_all_nicknames


class Executor(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Row(
            [
                self.exec_field(),
                self.all_nicknames,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START
            # expand=True,
            # width=600
        )

    def update_nicks(self, e):
        self.controls[0].controls[-1] = self.all_nicknames
        self.update()
        self.page.update()

    def exec_field(self):
        return ft.Row(
            [
                ft.ElevatedButton("Создать индивидуальную нагрузку", on_click=self.update_message_text),
                Text()
            ],
            vertical_alignment=ft.CrossAxisAlignment.START
        )

    def update_message_text(self, e):
        self.controls[0].controls[0].controls[-1].value = "Ожидайте..."
        self.update()

        self.controls[0].controls[0].controls[-1].value = make()
        self.update()

    @property
    def all_nicknames(self) -> ft.Column:
        return ft.Container(
            ft.Column([
                TitleText('Фамилии'),
                self.nicknames_column,
                ft.FloatingActionButton('Обновить', width=350, on_click=self.update_nicks)
            ])
        )

    @property
    def nicknames_column(self):
        return ft.ListView(
            [
                ft.Column(
                    [Text('"'+nick+'"') for nick in get_all_nicknames()]
                ),
            ],
            width=350,
            height=490,
        )
