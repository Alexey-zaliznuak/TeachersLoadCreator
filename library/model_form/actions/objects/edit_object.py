from typing import Union

from library.core.widgets.actions.table.edit_object import (
    EditObjectActionDialog,
    EditObjectActionButton,
)
from library.utils import LazyAttribute
from flet import Page

from .object_action import ObjectAction


class EditObjectAction(ObjectAction):
    action_widget = EditObjectActionButton

    def on_click_method(
        self,
        obj,
        page: Union[Page, LazyAttribute[Page]],
        datatable,
        e
    ):
        if isinstance(page, LazyAttribute):
            page = page()

        page.dialog = EditObjectActionDialog(
            obj=obj,
            datatable=datatable,
            form=datatable.form
        )
        page.dialog.open = True
        page.update()
