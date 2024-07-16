from typing import Union

from library.core.widgets.actions.table.edit_object import (
    EditObjectActionDialog,
)

from library.core.widgets.actions.objects.create_foreign import (
    CreateForeignObjectActionButton
)
from library.utils import LazyAttribute
from flet import Page, icons

from .object_action import ObjectAction


class CreateForeignObjectAction(ObjectAction):
    action_widget = CreateForeignObjectActionButton

    def __init__(self, foreign_form, foreign_field, *, icon=icons.EDIT):
        self.foreign_form = foreign_form
        self.foreign_field = foreign_field
        self.params = dict(icon=icon)

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
            form=self.foreign_form,
            obj={self.foreign_field.name: obj},
            datatable=datatable
        )
        page.dialog.open = True
        page.update()
