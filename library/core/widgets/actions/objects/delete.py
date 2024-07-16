from flet import (
    icons,
    colors
)


from library.core.widgets.actions import ActionButton


class DeleteObjectActionButtonWidget(ActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs,
            icon=icons.DELETE_OUTLINED,
            bgcolor=colors.RED
        )
