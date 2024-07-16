from flet import icons, AlertDialog, Container, Column, ElevatedButton, Text
from library.core.widgets.actions import ActionButton


class FilterActionButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs,
            icon=icons.FILTER_ALT_OUTLINED,
        )


class FilterActionDialog(AlertDialog):
    def __init__(self, datatable):
        self.datatable = datatable

        super().__init__(
            content=Container(
                content=Column(
                    controls=[
                        Text('Фильтрация'),
                        datatable.filterset.widget(),
                        ElevatedButton(
                            "Сохранить",
                            on_click=self._close_and_update,
                        ),
                    ]
                )
            )
        )

    def _close_and_update(self, e=None):
        self.datatable.update_rows()
        self.open = False
        self.page.update()
