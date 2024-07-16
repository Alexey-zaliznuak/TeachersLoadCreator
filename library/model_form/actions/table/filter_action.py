from library.core.widgets.actions.table import (
    FilterActionButton,
    FilterActionDialog
)

from .table_action import DataTableAction


class FilterAction(DataTableAction):
    action_widget = FilterActionButton

    def on_click_method(self, *args, datatable, form, **kwargs):
        datatable.page.dialog = FilterActionDialog(
            datatable=datatable,
        )
        datatable.page.dialog.open = True
        datatable.page.update()
