from flet import (
    AlertDialog,
    ElevatedButton,
    Text,
    MainAxisAlignment,
    SnackBar,
    colors,
)
from typing import Callable


class ConfirmActionDialog(AlertDialog):
    def __init__(
        self,
        on_success: Callable,
        on_cancel: Callable = lambda: None,
        *,
        success_snackbar: bool = True,
        success_snackbar_duration: int = 1600,
    ):
        self.on_success = on_success
        self.on_cancel = on_cancel

        self.success_snack_bar = success_snackbar
        self.success_snack_bar_duration = success_snackbar_duration

        super().__init__(
            modal=True,
            title=Text("Подтверждение"),
            content=Text("Пожалуйста, подтвердите действие."),
            actions=[
                ElevatedButton("Да", on_click=self.ok),
                ElevatedButton("Нет", on_click=self.cancel, color='red'),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def ok(self, e=None):
        self.on_success()
        if self.success_snack_bar:
            self.page.snack_bar = SnackBar(
                Text("Success.", size=18),
                duration=self.success_snack_bar_duration,
                bgcolor=colors.GREY,
                open=True
            )

        self.open = False
        self.page.update()

    def cancel(self, e=None):
        self.on_cancel()
        self.open = False
        self.page.update()
