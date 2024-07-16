from flet import (
    AlertDialog,
    BottomSheet,
    ElevatedButton,
    ImageFit,
    icons,
    MainAxisAlignment,
    Text,
    Control,
    Row,
    Container,
    Column,
    MainAxisAlignment,
    colors,
    border_radius,
    BoxShadow,
    ShadowBlurStyle,
    Offset,
    ListView,
    padding,
)
from typing import Callable
from library.core.widgets.text import Text, TitleText
from library.utils import LazyAttribute
from library.core.widgets import ErrorText
from library.model_form.fields import Field, empty
from library.core.widgets.actions import ActionButton
from peewee import Model


class EditFieldWidget(Container):
    def __init__(
        self,
        label: str,
        editing_field: Control = None,
        errors: Callable[[], list[str]] = None,
        help_text: str = None
    ):
        self.label = label
        self._get_errors = errors
        self.column_errors = Column(self._get_column_errors())

        labels = [Text(label)]
        if help_text:
            labels.append(Text(help_text))

        super().__init__(
            content=Column(
                [
                    *labels,
                    editing_field,
                    self.column_errors
                ]
            ),
            width=600,
        )

    def update(self):
        for child in self.content.controls:
            if child is self.column_errors:
                child.controls = self._get_column_errors()

        return super().update()

    def _get_column_errors(self) -> list[Control]:
        return [ErrorText(text) for text in self._get_errors()()]


class ObjectErrorBottomSheet(BottomSheet):
    def __init__(self, error_text: str):
        # todo max size? mb list view
        super().__init__(
            Container(
                Column([
                    Container(
                        Column([
                            TitleText("Данные невалидны:"),
                            Text(error_text)
                        ]),
                        padding=8,
                        bgcolor=colors.WHITE,
                        border_radius=16,
                        shadow=BoxShadow(
                            blur_radius=15,
                            color=colors.WHITE,
                            offset=Offset(0, 0),
                            blur_style=ShadowBlurStyle.OUTER,
                        )
                    ),
                    Row(
                        [
                            ElevatedButton(
                                "OK",
                                width=95,
                                height=45,
                                bgcolor=colors.AMBER_ACCENT_200,
                                on_click=self.close,
                            ),
                        ],
                        alignment=MainAxisAlignment.END
                    ),
                ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=30,
                expand=True,
                bgcolor=colors.BLUE_400,
                border_radius=border_radius.vertical(top=26, bottom=0),
            ),
            open=True,
            enable_drag=True,
        )

    def close(self, e=None):
        self.open = False
        self.update()


class EditObjectActionDialog(AlertDialog):
    def __init__(
        self,
        form,
        obj: dict = {},
        datatable=None,
        *args,
        create=None,
        **kwargs
    ):
        self.obj = obj
        self.create = False
        self.is_force_action = False

        if create is not None:
            self.create = create
            self.is_force_action = True

        self.form = form
        self.datatable = datatable
        self.errors: dict[str, list[str]] = {}
        self.fields: dict[Field, Control] = {}
        self.fields_widgets: list[Control] = self._get_content()

        assert isinstance(self.obj, (Model, dict))

        super().__init__(
            modal=True,
            # title=,
            content=Container(
                content=ListView(
                    [
                        TitleText(self.title_text),
                        Column(self.fields_widgets),
                        Container(
                            content=Row(
                                [
                                    ElevatedButton(
                                        "Закрыть",
                                        on_click=self._close_dlg,
                                    ),
                                    ElevatedButton(
                                        "Сохранить",
                                        on_click=self._save_obj,
                                    ),
                                ],
                                alignment=MainAxisAlignment.END,
                            ),
                            margin=10
                        ),
                    ],
                    width=600,
                    padding=padding.only(right=20)
                ),
                border_radius=26,
                padding=30,
                image_fit=ImageFit.COVER,
            ),
            title_padding=0,
            actions_padding=0,
            content_padding=0,
            actions_alignment=MainAxisAlignment.END,
        )

    def _get_content(self) -> list[Control]:
        # TODO : mb cached property
        # TODO normal annotate - list of widget[column(fields)], list fields
        controls = []

        for field in self.form._form_fields(read_only=False).values():
            if isinstance(self.obj, dict):
                value = self.obj.get(field.label, empty)
                # create action if no field value
                if not self.is_force_action and value is empty:
                    self.create = True

            else:
                value = getattr(self.obj, field.label, empty)

            edit_field = field.edit(value=value)
            self.fields[field] = edit_field
            controls.append(
                EditFieldWidget(
                    field.label,
                    edit_field,
                    LazyAttribute(
                        obj=self,
                        attr='errors.get',
                        args=(field.label, []),
                    ),
                    help_text=field.help_text
                )
            )
        return controls

    @property
    def title_text(self):
        if self.create:
            return f"Создать {self.form.Meta.model.__name__}"

        return f"Отредактировать {self.form.Meta.model.__name__}"

    def _close_dlg(self, e=None):
        self.open = False
        self.page.update()

    def _save_obj(self, e=None):
        new_obj = {}

        # TODO validators, some checks
        for ui_field, input_widget in self.fields.items():
            new_obj[ui_field.source] = input_widget.clear_value

        if self.create:
            _, object_error, self.errors = self.form.create(new_obj)
        else:
            _, object_error, self.errors = self.form.update(self.obj, new_obj)

        if not (self.errors or object_error):
            self.page.dialog.open = False
            self.page.update()
            self.datatable.update_rows()
            return

        if object_error:
            self.page.overlay.append(ObjectErrorBottomSheet(object_error))
            self.page.update()

        self.update()

    def update(self):
        for widget in self.fields_widgets:
            widget.update()

        return super().update()


class EditObjectActionButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs,
            icon=icons.EDIT,
            bgcolor=colors.GREY_100
        )
