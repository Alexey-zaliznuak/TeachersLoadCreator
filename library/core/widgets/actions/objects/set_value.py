from flet import (
    icons,
)


from library.core.widgets.actions import ActionButton


class SetValueObjectActionButtonWidget(ActionButton):
    def __init__(self, icon=icons.EDIT_ATTRIBUTES_OUTLINED, *args, **kwargs):
        super().__init__(
            *args, **kwargs,
            icon=icon,
        )
