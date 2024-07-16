import flet as ft
from itertools import cycle

CELL_WIDTH = 40
FIRST_COLUMN_WIDTH = 100
COLORS = [
    ft.colors.GREEN_ACCENT,
    ft.colors.LIGHT_BLUE_ACCENT_400,
    ft.colors.YELLOW_ACCENT,
    ft.colors.CYAN_300
]
get_colors = cycle(COLORS)


class TimeLine(ft.UserControl):
    def __init__(
        self,
        matrix,
    ):
        super().__init__()
        self.matrix = matrix

    def make_rectangles(self, data):
        row = []
        for rect in data:
            row.append(
                ft.canvas.Rect(
                    rect['start'],
                    rect['floor'],
                    rect['end'],
                    rect['height'],
                    paint=ft.Paint(
                        color=next(get_colors)
                    )
                )
            )
        return row

    def make_rows(self):
        rows = []
        for row in self.matrix:
            rows.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(row['name']),
                            width=FIRST_COLUMN_WIDTH,
                        ),
                        ft.Container(
                            content=ft.canvas.Canvas(
                                [
                                    *self.make_rectangles(
                                        row['data'],
                                    ),
                                    # ft.canvas.Rect(0,0,CELL_WIDTH* 24,10)
                                ],
                                width=float("inf"),
                                expand=True,
                            ),
                            height=40,
                            bgcolor=ft.colors.BLUE_400
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        return rows

    def build(self):
        return ft.ListView(
            [
                ft.Column([
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text('Помещение'),
                                width=FIRST_COLUMN_WIDTH,
                                alignment=ft.alignment.center
                            ),
                            *[
                                ft.Container(
                                    content=ft.Text(f'{hour:02}:00', size=12),
                                    width=CELL_WIDTH
                                ) for hour in range(24)
                            ]
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    ),
                    ft.Column(self.make_rows())
                ])
            ],
            # horizontal=True
        )
