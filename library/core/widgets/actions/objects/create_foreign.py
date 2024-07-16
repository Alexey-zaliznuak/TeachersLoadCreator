from flet import colors, icons
from library.core.widgets.actions import ActionButton


class CreateForeignObjectActionButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(dict(icon=icons.EDIT, bgcolor=colors.GREY_100) | kwargs),
        )
