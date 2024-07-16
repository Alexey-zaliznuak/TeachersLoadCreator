from typing import Callable, Sequence

from peewee import Model
from flet import (
    border,
    colors,
    DataTable,
    DataColumn,
    DataCell,
    DataRow,
    Text,
    Row,
)

from library.model_form.fields import Field
from library.model_form.actions import DataTableAction, ObjectAction
from library.utils import LazyAttribute
from library.model_form.filters import FilterSet, Filter


class UIModelFormDataTableCell(DataCell):
    def __init__(self, obj, field: Field, form, *args, **kwargs):
        # TODO paddings
        self.content = field.display(obj)
        self.form = form
        super().__init__(
            self.content,
            *args,
            **kwargs
        )


class UIModelFormDataTableObjectActionCell(DataCell):
    def __init__(self, actions: list[ObjectAction], *args, **kwargs):
        super().__init__(Row(actions), *args, **kwargs)


class UIModelFormDataTableObjectActionColumn(DataColumn):
    def __init__(self, col_name: str, *args, **kwargs):
        super().__init__(Text(col_name), *args, **kwargs)


class UIModelFormDataTableRow(DataRow):
    def __init__(
        self,
        obj,
        fields: list[Field],
        form,
        actions: list[ObjectAction],
        datatable: 'UIModelFormDataTable',
        row_number: int = 0,
        *args,
        **kwargs
    ):
        self.form = form
        cells = [
            UIModelFormDataTableCell(obj, field, form)
            for field in fields
        ]

        if actions:
            cells.append(DataCell(Row([
                action(
                    obj=obj,
                    datatable=datatable,
                    page=LazyAttribute(self, 'page'),
                ) for action in actions
            ])))

        kwargs = self.get_default_params(obj, row_number) | kwargs
        super().__init__(cells, *args, **kwargs)

    def get_default_params(self, obj, row_number: int):
        return {
            'color': (
                '#f2f2f2' if row_number % 2
                else colors.WHITE
            )
        }


class UIModelFormDataTableColumn(DataColumn):
    def __init__(self, label: str, field: Field, *args, **kwargs):
        numeric = getattr(field, 'numeric', False)
        tooltip = getattr(field, 'help_text', None) or label

        # TODO modal window with details of column type
        super().__init__(
            Text(label),
            numeric=numeric,
            tooltip=tooltip,
            *args,
            **kwargs
        )


class UIModelFormDataTable(DataTable):
    default = {
        'border': border.all(0.5, "transparent"),
        'border_radius': 3,
        'horizontal_lines': border.BorderSide(1, "transparent"),
        'vertical_lines': border.BorderSide(0.5, "transparent")
    }

    def __init__(
        self,
        columns: list[UIModelFormDataTableColumn],
        fields: list[Field],
        form,
        model: Model,
        queryset: Callable,
        filterset: FilterSet = None,
        default_filters: Sequence[Filter] = (),
        objects_actions: Sequence[ObjectAction] = (),
        table_actions: Sequence[DataTableAction] = (),
        action_column: DataColumn = DataColumn(Text('Actions')),
        get_row_params: Callable = None,
        **kwargs,
    ):
        self.fields = fields
        self.filterset = None
        if filterset:
            self.filterset = filterset(form, self)

        self.default_filters = default_filters
        self.form = form
        self.model = model
        self.objects_actions = objects_actions
        self.queryset = queryset
        self.table_actions = table_actions
        self.get_row_params = get_row_params

        self.update_rows()

        if action_column and objects_actions:
            columns.append(action_column)

        kwargs = (self.default | kwargs)
        super().__init__(columns=columns, rows=self.rows, **kwargs)

    def update_rows(self, only_self_content_update: bool = False):
        self.rows = [
            UIModelFormDataTableRow(
                obj=obj,
                fields=self.fields,
                actions=self.objects_actions,
                datatable=self,
                form=self.form,
                row_number=row_number,
                **(
                    self.get_row_params(obj, self, self.form)
                    if self.get_row_params
                    else {}
                )
            )
            for row_number, obj in enumerate(self._get_queryset())
        ]

        if hasattr(self, 'page'):
            if not only_self_content_update:
                for datatable in self.page.datatables:
                    try:
                        datatable.update_rows(only_self_content_update=True)
                    except Exception:
                        pass
            self.update()

    def _get_queryset(self):
        queryset = self.queryset()

        for f in self.default_filters:
            queryset = f.filter(queryset)

        if self.filterset:
            queryset = self.filterset.filter(queryset)

        return queryset
