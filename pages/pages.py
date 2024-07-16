import flet as ft

from widgets.CustomNavigation import CustomNavigation


def WorkPage(WorkTypesFormDataTable, TaskFormDataTable):
    return CustomNavigation(
        selected_index=0,
        routes=[
            {
                "icon": (
                    ft.icons.REQUEST_QUOTE,
                    ft.icons.REQUEST_QUOTE_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[TaskFormDataTable]),
                'title': 'Заявки'
            },
            {
                "icon": (
                    ft.icons.NOW_WIDGETS,
                    ft.icons.NOW_WIDGETS_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[WorkTypesFormDataTable]),
                'title': 'Виды работ'
            },
        ],
    )


def BookingPage(BookingFormDataTable, TimeLineTable):
    return CustomNavigation(
        selected_index=0,
        routes=[
            {
                "icon": (
                    ft.icons.FACT_CHECK,
                    ft.icons.FACT_CHECK_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[BookingFormDataTable]),
                'title': 'Бронь'
            },
            {
                "icon": (
                    ft.icons.CALENDAR_VIEW_DAY,
                    ft.icons.CALENDAR_VIEW_DAY_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[TimeLineTable]),
                'title': 'Календарь бронирования'
            },
        ],
    )


def EducationPage(
    EventFormDataTable,
    PlaceDataTable,
    EventTypesDataTable,
    WorkTypesFormDataTable,
    TaskFormDataTable,
    BookingFormDataTable,
    TimeLineTable
):
    return CustomNavigation(
        selected_index=0,
        routes=[
            {
                "icon": (
                    ft.icons.EVENT,
                    ft.icons.EVENT_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[EventFormDataTable]),
                'title': 'Мероприятия'
            },
            {
                "icon": (
                    ft.icons.PLACE,
                    ft.icons.PLACE_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[PlaceDataTable]),
                'title': 'Пространства'
            },
            {
                "icon": (
                    ft.icons.NOW_WIDGETS,
                    ft.icons.NOW_WIDGETS_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[EventTypesDataTable]),
                'title': 'Виды мероприятий'
            },
            {
                "icon": (
                    ft.icons.WORK,
                    ft.icons.WORK_OUTLINED,
                ),
                'page':
                    WorkPage(WorkTypesFormDataTable, TaskFormDataTable),
                'title': ''
            },
            {
                "icon": (
                    ft.icons.EDIT_CALENDAR,
                    ft.icons.EDIT_CALENDAR_OUTLINED,
                ),
                'page':
                    BookingPage(BookingFormDataTable, TimeLineTable),
                'title': ''
            },
        ],
    )


def LearningPage(
    EventFormDataTable,
    PlaceDataTable,
    EventTypesDataTable,
    WorkTypesFormDataTable,
    TaskFormDataTable,
    BookingFormDataTable,
    TimeLineTable
):
    return CustomNavigation(
        selected_index=0,
        routes=[
            {
                "icon": (
                    ft.icons.EVENT,
                    ft.icons.EVENT_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[EventFormDataTable]),
                'title': 'Мероприятия'
            },
            {
                "icon": (
                    ft.icons.PLACE,
                    ft.icons.PLACE_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[PlaceDataTable]),
                'title': 'Пространства'
            },
            {
                "icon": (
                    ft.icons.NOW_WIDGETS,
                    ft.icons.NOW_WIDGETS_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[EventTypesDataTable]),
                'title': 'Виды мероприятий'
            },
            {
                "icon": (
                    ft.icons.WORK,
                    ft.icons.WORK_OUTLINED,
                ),
                'page':
                    WorkPage(WorkTypesFormDataTable, TaskFormDataTable),
                'title': ''
            },
            {
                "icon": (
                    ft.icons.EDIT_CALENDAR,
                    ft.icons.EDIT_CALENDAR_OUTLINED,
                ),
                'page':
                    BookingPage(BookingFormDataTable, TimeLineTable),
                'title': ''
            },
        ]
    )


def EntertainmentPage(
    PlaceDataTable,
    TeacherFormDataTable,
    ClubFormDataTable,
    ClubTypeFormDataTable,
):
    return CustomNavigation(
        selected_index=2,
        routes=[
            {
                "icon": (
                    ft.icons.PLACE,
                    ft.icons.PLACE_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[PlaceDataTable]),
                'title': 'Пространства'
            },
            {
                "icon": (
                    ft.icons.MAN,
                    ft.icons.MAN_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[TeacherFormDataTable]),
                'title': 'Учителя'
            },
            {
                "icon": (
                    ft.icons.THEATER_COMEDY,
                    ft.icons.THEATER_COMEDY_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[ClubFormDataTable]),
                'title': 'Кружки'
            },
            {
                "icon": (
                    ft.icons.NOW_WIDGETS,
                    ft.icons.NOW_WIDGETS_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[ClubTypeFormDataTable]),
                'title': 'Виды кружков'
            },
        ]
    )


def WorkTablePage(WorkTable):
    return CustomNavigation(
        selected_index=0,
        routes=[
            {
                "icon": (
                    ft.icons.WORK,
                    ft.icons.WORK_OUTLINED,
                ),
                'page':
                    ft.ListView(controls=[WorkTable]),
                'title': 'Заявки'
            },
        ]
    )
