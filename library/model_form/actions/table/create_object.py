from library.core.widgets.actions.table import CreateObjectActionButtonWidget
from library.core.widgets.actions.table import EditObjectActionDialog

from .table_action import DataTableAction


class CreateObjectAction(DataTableAction):
    action_widget = CreateObjectActionButtonWidget

    def on_click_method(self, *args, datatable, form, **kwargs):
        datatable.page.dialog = EditObjectActionDialog(
            datatable=datatable,
            form=form,
        )
        datatable.page.dialog.open = True
        datatable.page.update()
