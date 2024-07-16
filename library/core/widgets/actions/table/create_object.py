from flet import (
    icons,
)
from library.core.widgets.actions import ActionButton


class CreateObjectActionButtonWidget(ActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs,
            icon=icons.ADD,
        )
