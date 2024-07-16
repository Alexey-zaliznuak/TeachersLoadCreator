import flet as ft
from datetime import datetime
from core.TimeLineTable.TimeLine import TimeLine
from core.TimeLineTable.TimeLineDataFormatter import TimeLineDataFormatter

from library.core.widgets.fields.DateTime import DatePicker


class TimeLineTable(ft.UserControl):
    def __init__(
        self,
        get_bookings,
        get_places
    ):
        self.bookings = get_bookings
        self.places = get_places

        self.datepicker = DatePicker(
            value=datetime.now(),
            on_change=self.on_change
        )

        self.time_line_data_formatter = TimeLineDataFormatter(
            get_bookings=get_bookings,
            get_places=get_places
        )

        super().__init__()

    def get_matrix(self):
        return self.time_line_data_formatter.get_rows()

    def on_change(self, value):
        self.time_line_data_formatter.select_day = value

        self.TimeLine = TimeLine(
            self.get_matrix()
        )
        self.controls[0].content.controls[1].content = self.TimeLine
        self.update()

    def build(self):
        self.TimeLine = TimeLine(
            self.get_matrix()
        )

        return (
            ft.Container(
                content=ft.Column(
                    [
                        self.datepicker,
                        ft.Container(
                            content=self.TimeLine
                        )
                    ]
                )
            )
        )
