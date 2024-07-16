import locale as loc
import flet as ft
import calendar
from typing import Optional, Union
from datetime import datetime, timedelta

from .selection_type import SelectionType

PREV_MONTH = "PM"
NEXT_MONTH = "NM"
PREV_YEAR = "PY"
NEXT_YEAR = "NY"

PREV_HOUR = "PH"
NEXT_HOUR = "NH"
PREV_MINUTE = "PMIN"
NEXT_MINUTE = "NMIN"

EMPTY = ""
WHITE_SPACE = " "

DELTA_MONTH_WEEK = 5
DELTA_YEAR_WEEK = 52
DELTA_HOUR = 1
DELTA_MINUTE = 1

WEEKEND_DAYS = [5, 6]

CELL_SIZE = 32
LAYOUT_WIDTH = 340
LAYOUT_MIN_HEIGHT = 280
LAYOUT_MAX_HEIGHT = 320
LAYOUT_DT_MIN_HEIGHT = 320
LAYOUT_DT_MAX_HEIGHT = 360


class DateWidget(ft.UserControl):

    @property
    def selected_data(self):
        return self.selected

    def __init__(
        self,
        hour_minute: bool = False,
        selected_date: Optional[list[datetime]] = None,
        selection_type: Union[SelectionType, int] = SelectionType.SINGLE,
        disable_to: datetime = None,
        disable_from: datetime = None,
        holidays: list[datetime] = None,
        hide_prev_next_month_days: bool = False,
        first_weekday: int = 0,
        show_three_months: bool = False,
        locale: str = 'ru_RU.UTF-8',
        on_change=None
    ):
        super().__init__()

        self.selected = selected_date
        if (
            (not hour_minute)
            or (not isinstance(selected_date[0], datetime) and hour_minute)
        ):
            self.selected = list(
                map(
                    lambda n_date:
                        datetime.combine(
                            n_date,
                            datetime.min.time()
                        ),
                    selected_date
                )
            ) or []

        self.selection_type = SelectionType(selection_type)
        self.hour_minute = hour_minute
        self.disable_to = disable_to
        self.disable_from = disable_from
        self.holidays = holidays
        self.hide_prev_next_month_days = hide_prev_next_month_days
        self.first_weekday = first_weekday
        self.show_three_months = show_three_months
        self.on_change = on_change

        if locale:
            loc.setlocale(loc.LC_ALL, locale)

        self.now = datetime.combine(datetime.now(), datetime.min.time())
        self.yy = self.now.year
        self.mm = self.now.month
        self.dd = self.now.day
        self.hour = datetime.min.hour
        self.minute = datetime.min.minute

        if hour_minute and self.selected:
            self.hour = self.selected[0].hour
            self.minute = self.selected[0].minute

        self.cal = calendar.Calendar(first_weekday)

    def _get_current_month(self, year, month):
        return self.cal.monthdatescalendar(year, month)

    def _create_calendar(self, year, month, hour, minute, hide_ymhm=False):

        week_rows_controls = []
        week_rows_days_controls = []
        today = datetime.now()

        days = self._get_current_month(year, month)

        ym = self._year_month_selectors(year, month, hide_ymhm)
        week_rows_controls.append(
            ft.Column(
                [ym],
                alignment=ft.MainAxisAlignment.START
            )
        )

        labels = ft.Row(self._row_labels(), spacing=18)
        week_rows_controls.append(
            ft.Column(
                [labels],
                alignment=ft.MainAxisAlignment.START
            )
        )

        weeks_rows_num = len(self._get_current_month(year, month))
        for w in range(weeks_rows_num):
            row = []

            for d in days[w]:

                if self.hour_minute:
                    d = datetime(
                        d.year,
                        d.month,
                        d.day,
                        self.hour,
                        self.minute,
                    )
                else:
                    d = datetime(d.year, d.month, d.day)

                month = d.month
                is_main_month = True if month == self.mm else False

                if self.hide_prev_next_month_days and not is_main_month:
                    row.append(
                        ft.Text(
                            "",
                            width=CELL_SIZE,
                            height=CELL_SIZE,
                        )
                    )
                    continue

                dt_weekday = d.weekday()
                day = d.day
                is_weekend = False
                is_holiday = False

                is_day_disabled = False

                if (
                    self.disable_from
                    and self._trunc_datetime(d)
                    > self._trunc_datetime(self.disable_from)
                ):
                    is_day_disabled = True

                if (
                    self.disable_to
                    and self._trunc_datetime(d)
                    < self._trunc_datetime(self.disable_to)
                ):
                    is_day_disabled = True

                text_color = None
                border_side = None
                bg = None
                # week end bg color
                if dt_weekday in WEEKEND_DAYS:
                    text_color = ft.colors.RED_500
                    is_weekend = True
                # holidays
                if self.holidays and d in self.holidays:
                    text_color = ft.colors.RED_500
                    is_holiday = True

                # current day bg
                if (
                    is_main_month
                    and day == self.dd
                    and self.dd == today.day
                    and self.mm == today.month
                    and self.yy == today.year
                ):
                    border_side = ft.BorderSide(2, ft.colors.BLUE)
                elif (
                    (is_weekend or is_holiday)
                    and (not is_main_month or is_day_disabled)
                ):
                    text_color = ft.colors.RED_200
                    bg = None
                elif not is_main_month and is_day_disabled:
                    text_color = ft.colors.BLACK38
                    bg = None
                elif not is_main_month:
                    text_color = ft.colors.BLUE_200
                    bg = None
                else:
                    bg = None

                # selected days
                datepicker_date = d.date()
                selected_date = list(
                    map(lambda day: day.date(), self.selected)
                )

                selected_numbers = len(selected_date)

                if (self.selection_type != SelectionType.RANGE):
                    if (
                        selected_numbers > 0
                        and datepicker_date in selected_date
                    ):
                        bg = ft.colors.BLUE_400
                        text_color = ft.colors.WHITE
                else:
                    if (
                        selected_numbers > 0
                        and selected_numbers < 3
                        and datepicker_date in selected_date
                    ):
                        bg = ft.colors.BLUE_400
                        text_color = ft.colors.WHITE

                if (
                    self.selection_type == SelectionType.RANGE
                    and selected_numbers > 1
                ):
                    if (
                        datepicker_date > selected_date[0]
                        and datepicker_date < selected_date[-1]
                    ):
                        bg = ft.colors.BLUE_300
                        text_color = ft.colors.WHITE

                row.append(
                    ft.TextButton(
                        text=str(day),
                        data=d,
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        disabled=is_day_disabled,
                        style=ft.ButtonStyle(
                            color=text_color,
                            bgcolor=bg,
                            padding=0,
                            shape={
                                ft.MaterialState.DEFAULT:
                                    ft.RoundedRectangleBorder(radius=20),
                            },
                            side=border_side
                        ),
                        on_click=self._select_date
                    )
                )

            week_rows_days_controls.append(ft.Row(row, spacing=18))

        week_rows_controls.append(
            ft.Column(
                week_rows_days_controls,
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            )
        )

        if self.hour_minute and not hide_ymhm:
            hm = self._hour_minute_selector(hour, minute)
            week_rows_controls.append(
                ft.Row(
                    [hm],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )

        return week_rows_controls

    def _year_month_selectors(self, year, month, hide_ymhm=False):
        if not hide_ymhm:
            prev_year = ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                data=PREV_YEAR,
                on_click=self._adjust_calendar
            )
            next_year = ft.IconButton(
                icon=ft.icons.ARROW_FORWARD,
                data=NEXT_YEAR,
                on_click=self._adjust_calendar
            )
            prev_month = ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                data=PREV_MONTH,
                on_click=self._adjust_calendar
            )
            next_month = ft.IconButton(
                icon=ft.icons.ARROW_FORWARD,
                data=NEXT_MONTH,
                on_click=self._adjust_calendar
            )
        else:
            prev_year = ft.Text(
                EMPTY,
                height=CELL_SIZE,
            )
            next_year = ft.Text(EMPTY)
            prev_month = ft.Text(EMPTY)
            next_month = ft.Text(EMPTY)

        ym = ft.Row([
            ft.Row([
                prev_year,
                ft.Text(year),
                next_year,
            ], spacing=0),
            ft.Row([
                prev_month,
                ft.Text(
                    calendar.month_name[month],
                    text_align=ft.alignment.center
                ),
                next_month,
            ], spacing=0),
        ],
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        return ym

    def _row_labels(self):
        label_row = []
        days_label = calendar.weekheader(2).split(WHITE_SPACE)

        for _ in range(0, self.first_weekday):
            days_label.append(days_label.pop(0))

        for day in days_label:
            label_row.append(
                ft.TextButton(
                    text=day,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    disabled=True,
                    style=ft.ButtonStyle(
                        padding=0,
                        color=ft.colors.BLACK,
                        bgcolor=ft.colors.GREY_300,
                        shape={
                            ft.MaterialState.DEFAULT:
                                ft.RoundedRectangleBorder(radius=20),
                        }
                    )
                )
            )

        return label_row

    def _hour_minute_selector(self, hour, minute):
        selector = ft.Row(
            [
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        data=PREV_HOUR,
                        on_click=self._adjust_hh_min
                    ),
                    ft.Text(hour),
                    ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD,
                        data=NEXT_HOUR,
                        on_click=self._adjust_hh_min
                    ),
                ]),
                ft.Text(":"),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        data=PREV_MINUTE,
                        on_click=self._adjust_hh_min,
                    ),
                    ft.Text(minute),
                    ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD,
                        data=NEXT_MINUTE,
                        on_click=self._adjust_hh_min,
                    ),
                ]),
            ],
            spacing=48,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

        return selector

    def build(self):

        rows = self._create_layout(self.yy, self.mm, self.hour, self.minute)

        cal_height = self._calculate_height(self.yy, self.mm)

        self.cal_container = ft.Container(
            content=ft.Row(rows),
            bgcolor=ft.colors.WHITE,
            padding=12,
            height=self._cal_height(cal_height)
        )
        return self.cal_container

    def _calculate_height(self, year, month):
        if self.show_three_months:
            prev, next = self._prev_next_month(year, month)
            cal_height = max(
                len(self._get_current_month(year, month)),
                len(self._get_current_month(prev.year, prev.month)),
                len(self._get_current_month(next.year, next.month))
            )
        else:
            cal_height = len(self._get_current_month(year, month))
        return cal_height

    def _create_layout(self, year, month, hour, minute):
        rows = []
        prev, next = self._prev_next_month(year, month)

        if self.show_three_months:
            week_rows_controls_prev = self._create_calendar(
                prev.year, prev.month, hour, minute, True)
            rows.append(ft.Column(week_rows_controls_prev,
                        width=LAYOUT_WIDTH, spacing=10))
            rows.append(ft.VerticalDivider())

        week_rows_controls = self._create_calendar(year, month, hour, minute)
        rows.append(ft.Column(week_rows_controls,
                    width=LAYOUT_WIDTH, spacing=10))

        if self.show_three_months:
            rows.append(ft.VerticalDivider())
            week_rows_controls_next = self._create_calendar(
                next.year, next.month, hour, minute, True)
            rows.append(ft.Column(week_rows_controls_next,
                        width=LAYOUT_WIDTH, spacing=10))

        return rows

    def _prev_next_month(self, year, month):
        delta = timedelta(weeks=DELTA_MONTH_WEEK)
        current = datetime(year, month, 15)
        prev = current - delta
        next = current + delta
        return prev, next

    def _select_date(self, e: ft.ControlEvent):

        result: datetime = e.control.data

        if self.selection_type == SelectionType.RANGE:
            if len(self.selected) == 2:
                self.selected = []

            if len(self.selected) > 0:
                if result <= self.selected[0] or len(self.selected) != 1:
                    return
                if self.selected[0] == result:
                    self.selected = []
                    return
                self.selected.append(result)
                return
            else:
                self.selected.append(result)
        elif self.selection_type == SelectionType.MULTIPLE:
            if len(self.selected) > 0 and result in self.selected:
                self.selected.remove(result)
            else:
                if self.hour_minute:
                    result = datetime(
                        result.year,
                        result.month,
                        result.day,
                        self.hour,
                        self.minute
                    )
                self.selected.append(result)
        else:
            if not (len(self.selected) == 1 and result in self.selected):
                self.selected = []
                if self.hour_minute:
                    result = datetime(result.year, result.month,
                                      result.day, self.hour, self.minute)
                self.selected.append(result)

        self._update_calendar()

    def _adjust_calendar(self, e: ft.ControlEvent):

        if (
            e.control.data == PREV_MONTH
            or e.control.data == NEXT_MONTH
        ):
            delta = timedelta(weeks=DELTA_MONTH_WEEK)
        if (
            e.control.data == PREV_YEAR
            or e.control.data == NEXT_YEAR
        ):
            delta = timedelta(weeks=DELTA_YEAR_WEEK)
        if (
            e.control.data == PREV_MONTH
            or e.control.data == PREV_YEAR
        ):
            self.now = self.now - delta
        if (
            e.control.data == NEXT_MONTH
            or e.control.data == NEXT_YEAR
        ):
            self.now = self.now + delta

        self.mm = self.now.month
        self.yy = self.now.year
        self._update_calendar()

    def _adjust_hh_min(self, e: ft.ControlEvent):

        if (
            e.control.data == PREV_HOUR
            or e.control.data == NEXT_HOUR
        ):
            delta = timedelta(hours=DELTA_HOUR)
        if (
            e.control.data == PREV_MINUTE
            or e.control.data == NEXT_MINUTE
        ):
            delta = timedelta(minutes=DELTA_MINUTE)
        if (
            e.control.data == PREV_HOUR
            or e.control.data == PREV_MINUTE
        ):
            self.now = self.now - delta
        if (
            e.control.data == NEXT_HOUR
            or e.control.data == NEXT_MINUTE
        ):
            self.now = self.now + delta

        self.hour = self.now.hour
        self.minute = self.now.minute

        self.selected_data[0] = datetime.combine(
            self.selected_data[0], self.now.time()
        )
        self._update_calendar()

    def _update_calendar(self):
        self.cal_container.content = ft.Row(
            self._create_layout(self.yy, self.mm, self.hour, self.minute))
        cal_height = self._calculate_height(self.yy, self.mm)
        self.cal_container.height = self._cal_height(cal_height)
        if self.on_change:
            self.on_change(value=self.selected_data[0])
        self.update()

    def _cal_height(self, weeks_number):
        if self.hour_minute:
            return LAYOUT_DT_MIN_HEIGHT if (
                weeks_number == 5
            ) else (
                LAYOUT_DT_MAX_HEIGHT
            )
        else:
            return LAYOUT_MIN_HEIGHT if (
                weeks_number == 5
            ) else (
                LAYOUT_MAX_HEIGHT
            )

    def _trunc_datetime(self, date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)
