import flet as ft
from ..datepicker.datepicker import DateWidget
from ..datepicker.selection_type import SelectionType
from datetime import datetime, date, time
from .Text import TextViewer
from .BaseViewer import Viewer
from .BaseInput import InputField


class DateTimeClass(ft.UserControl):
    holidays = [
        datetime(2023, 4, 25),
        datetime(2023, 5, 1),
        datetime(2023, 6, 2),
    ]

    def __init__(
        self,
        value: str,
        width: ft.OptionalNumber = None,
        hour_minute: bool = False,
        show_three_months: bool = False,
        hide_no_month: bool = False,
        datepicker_type: int = 0,
    ):
        super().__init__()

        self.value = self._to_datetime(value)
        self.type = SelectionType.SINGLE.value
        self.datepicker = None
        self.width = width
        self.selected_locale = None
        self.datepicker_type = datepicker_type
        self.hour_minute = hour_minute
        self.show_three_months = show_three_months
        self.hide_no_month = hide_no_month

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Календарь"),
            actions=[
                ft.TextButton("Закрыть", on_click=self.cancel_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=5,
            content_padding=0
        )

        if value is None:
            value = datetime.now()

        if not isinstance(value, str):
            if self.hour_minute:
                value = datetime.strftime(value, "%Y-%m-%d\n%H:%M")
            else:
                value = datetime.strftime(value, "%Y-%m-%d")

        self.tf = ft.Container(
            content=ft.Text(
                value=value,
            ),
            width=120,
            height=50,
            alignment=ft.alignment.center_left,
        )

        self.cal_ico = ft.TextButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=self.open_dlg_modal,
            height=50,
            width=40,
            right=0,
            style=ft.ButtonStyle(
                shape={
                    ft.MaterialState.DEFAULT:
                    ft.RoundedRectangleBorder(radius=1),
                },
            ))

        self.st = ft.Stack(
            [
                self.tf,
                self.cal_ico,
            ],
            width=120
        )

    def build(self):
        return ft.Container(
            content=self.st,
        )

    def confirm_dlg(self, e):
        if int(self.type) == SelectionType.SINGLE.value:
            self.tf.value = self.datepicker.selected_data[0] if len(
                self.datepicker.selected_data) > 0 else None
        elif (
            int(self.type) == SelectionType.MULTIPLE.value
            and len(self.datepicker.selected_data) > 0
        ):
            self.from_to_text.value = "[" + ", ".join(
                [d.isoformat() for d in self.datepicker.selected_data]) + "]"
            self.from_to_text.visible = True
        elif (
            int(self.type) == SelectionType.RANGE.value
            and len(self.datepicker.selected_data) > 0
        ):
            self.from_to_text.value = (
                f"From: {self.datepicker.selected_data[0]} "
                f"To: {self.datepicker.selected_data[1]}"
            )
            self.from_to_text.visible = True

        self.dlg_modal.open = False
        self.update()

    def cancel_dlg(self, e):
        self.page.dialog.open = False
        self.page.update()

    def open_dlg_modal(self, e):
        self.datepicker = DateWidget(
            hour_minute=self.hour_minute,
            show_three_months=self.show_three_months,
            hide_prev_next_month_days=False,
            selected_date=[self.value] if self.value else None,
            selection_type=self.datepicker_type,
            holidays=self.holidays,
            # disable_to=self._to_datetime(self.tf1.value),
            # disable_from=self._to_datetime(self.tf2.value),
            # locale=self.selected_locale,
        )
        if not (self.page.dialog and self.page.dialog.open):
            self.page.dialog = self.dlg_modal
            self.dlg_modal.content = self.datepicker
            self.dlg_modal.open = True
        self.page.update()
        self.update()

    def _to_datetime(self, dt):
        if isinstance(dt, (datetime, date)):
            return dt

        if not dt:
            if getattr(self, 'hour_minute', False):
                return datetime.now()
            else:
                return date.today()

        if getattr(self, 'hour_minute', False):
            return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")

        return datetime.strptime(dt, "%Y-%m-%d")

    def set_locale(self, e):
        self.selected_locale = self.dd.value or None


class DateViewer(DateTimeClass, Viewer):
    pass


class DateTimeViewer(DateViewer):
    defaults = {
        'hour_minute': True,
    }

    def __init__(self, *args, **kwargs):
        kwargs = kwargs | self.defaults
        super().__init__(*args, **kwargs)


class DatePicker(DateTimeClass, InputField):
    def __init__(
        self,
        value: datetime,
        hour_minute: bool = False,
        show_three_months: bool = False,
        hide_no_month: bool = False,
        datepicker_type: int = 0,
        on_change=None
    ):

        super().__init__(value=value)
        self.value = self._to_datetime(value)
        self.datepicker_type = datepicker_type
        self.hour_minute = hour_minute
        self.show_three_months = show_three_months
        self.hide_no_month = hide_no_month
        self.on_change = on_change

    def build(self):
        self.datepicker = DateWidget(
            hour_minute=self.hour_minute,
            show_three_months=self.show_three_months,
            hide_prev_next_month_days=False,
            selected_date=[self.value] if self.value else None,
            selection_type=self.datepicker_type,
            holidays=self.holidays,
            on_change=self.on_change
        )

        return self.datepicker

    @property
    def clear_value(self):
        return self.datepicker.selected_data[0]


class DateTimePicker(DateWidget):
    defaults = {
        'hour_minute': True,
    }

    def __init__(self, *args, **kwargs):
        kwargs = kwargs | self.defaults
        super().__init__(*args, **kwargs)


class TimePicker(ft.ElevatedButton, InputField):
    def __init__(
        self,
        value: str
    ):
        value = value or '0:0'
        h, m = value.split(':')
        value = time(hour=int(h), minute=int(m))

        self.flag = False
        self.time_picker = ft.TimePicker(
            confirm_text="Готово",
            cancel_text="Отмена",
            error_invalid_text="Неправильно время",
            help_text="Выбери время",
            on_change=self.time_change,
            value=value
        )

        super().__init__(
            self.time_to_text(value),
            icon=ft.icons.ACCESS_TIME,
            on_click=lambda _: self.pick_time(),
        )

    def time_change(self, e):
        self.text = self.time_to_text(self.time_picker.value)
        self.update()

    def time_to_text(self, time):
        return f"{time.hour:02}:{time.minute:02}"

    def pick_time(self):
        if not self.flag:
            self.page.overlay.append(self.time_picker)
            self.page.update()
        self.flag = True

        self.time_picker.pick_time()

    @property
    def clear_value(self):
        return self.time_picker.value


class TimeViewer(TextViewer, Viewer):
    def __init__(self, value):
        value = str(value).split(':')
        value = f"{value[0]:02}:{value[1]:02}"

        super().__init__(value=value)
