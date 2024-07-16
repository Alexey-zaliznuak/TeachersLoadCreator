from functools import partial

from flet import Control


from library.core.widgets.actions import ActionButton


class DataTableAction():
    """Action class for doing smth with no one object."""
    action_widget: ActionButton = None

    def __call__(self, datatable=None, form=None) -> Control:
        return self.action_widget(
            partial(self.on_click_method, datatable=datatable, form=form)
        )

    def on_click_method(self, *args, **kwargs):
        ...
