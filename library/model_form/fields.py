from flet import Control
from datetime import datetime
from types import FunctionType

from library.core.validators import (
    URLValidator,
    PhoneValidator,
    ForeignKeyValidator,
    DaysFieldDefaultValidator,
)
from library.core.exceptions import ValidationError
from library.core.widgets.fields.DateTime import TimePicker
from library.core.widgets.fields.DaysPicker import DaysAndCounterPicker, DaysViewer
from library.types import empty
from library.core.widgets.fields import (
    BooleanViewer,
    BooleanInput,
    DateViewer,
    DatePicker,
    ForeignKeyViewer,
    ForeignKeyEditor,
    MultiLineTextViewer,
    MultiLineTextEditor,
    PhoneInput,
    PhoneViewer,
    TextViewer,
    TextEditor,
    TimeViewer,
    DateTimePicker,
    DateTimeViewer,
    IntegerInput,
)


class Field:
    """Base class for all field types."""

    numeric = False

    default_validators = []
    # default_empty_value = '' TODO mb delete if useless
    default_error_messages = {
        'required': 'Это поле обязательно',
        'null': 'Не может быть пустым'
    }

    initial_empty_value = None
    edit_widget: Control = TextEditor
    display_widget: Control = TextViewer

    def __init__(
        self,
        source: str,
        read_only=False,
        write_only=False,
        required: bool = None,
        default=empty,
        label: str = '',
        help_text: str = None,
        style=None,
        error_messages: dict = None,
        validators: list = [],
        allow_null=False,
    ):
        # TODO mb model in mapping in future
        # If `required` is unset, then use `True` unless a default is provided.
        if required is None:
            required = default is empty and not read_only

        # Some combinations of keyword arguments do not make sense.
        assert not (read_only and write_only), (
            'Невалидная комбинация полей: '
            f'Только чтение - {read_only} и только  запись - {write_only}'
        )
        assert not (read_only and required), (
            'Invalid combination of fields values: read_only and required'
            f'Только чтение - {read_only} и обязательное - {required}'
        )
        assert not (required and default is not empty), (
            'Invalid combination of fields values: required and default'
            f'обязательно - {required} и по умолчанию - {default}'
        )

        self.read_only = read_only
        self.write_only = write_only
        self.required = required
        self.source = source
        self.label = label or source
        self.help_text = help_text
        self.style = style or {}
        self.allow_null = allow_null
        self.validators = validators.copy()
        self.validators.extend(self.default_validators)

        self.initial = self.initial_empty_value
        self.initial = (
            self.initial() if callable(self.initial) else self.initial
        )

        default = default() if callable(default) else default

        if not isinstance(default, empty):
            self.initial = default

        self.field_name = None

        self.error_messages = error_messages

    def validate(self, value) -> list[str]:
        errors = []

        # rodo mb feature wu=ith required
        if value is None and not self.allow_null:
            errors.append('Обязательное поле')

        for validator in self.validators:
            try:
                validator(value)
            except ValidationError as e:
                errors.append(e)

        return errors

    def clear(self, value):
        return value

    def _get_db_value(self, obj):
        return getattr(obj, self.source)

    def _get_display_value(self, obj):
        return self._get_db_value(obj)

    def _get_editing_default_value(self, obj):
        return self._get_db_value(obj)

    def edit(self, *, value=empty, obj=empty) -> Control:
        value = self._get_edit_value(value=value, obj=obj)
        return self.edit_widget(value)

    def display(self, obj) -> Control:
        value = self._get_display_value(obj)
        return self.display_widget(value)

    def _get_edit_value(self, *, value, obj):
        assert not (value is not empty and obj is not empty), (
            "Может быть указано только одно из значений 'поле' и 'объект'."
        )

        if obj is not empty:
            value = self._get_editing_default_value(obj)

        elif value is empty:
            value = self.initial

        return value


class BooleanField(Field):
    display_widget = BooleanViewer
    edit_widget = BooleanInput


class CharField(Field):
    def edit(self, *, value=empty, obj=empty) -> Control:
        value = self._get_edit_value(value=value, obj=obj)
        return self.edit_widget(value=value)


class PhoneField(Field):
    initial_empty_value = ''
    display_widget = PhoneViewer
    edit_widget = PhoneInput
    default_validators = [PhoneValidator()]


class DaysField(CharField):
    def __init__(
        self,
        source: str,
        read_only=False,
        write_only=False,
        required: bool = None,
        default=empty,
        label: str = '',
        help_text: str = None,
        style=None,
        error_messages: dict = None,
        validators: list = [],
        allow_null=False
    ):
        super().__init__(
            source,
            read_only,
            write_only,
            required,
            default,
            label,
            help_text,
            style,
            error_messages,
            validators,
            allow_null
        )
        self.default_validators = [DaysFieldDefaultValidator()]
    display_widget = DaysViewer
    edit_widget = DaysAndCounterPicker


class ChooseField(Field):  # ???? ValueValidator?
    ...


class TimeField(Field):
    display_widget = TimeViewer
    edit_widget = TimePicker


class DateField(Field):
    display_widget = DateViewer
    edit_widget = DatePicker
    initial_empty_value = datetime.today


class DateTimeField(Field):
    display_widget = DateTimeViewer
    edit_widget = DateTimePicker
    # initial_empty_value = datetime.date


class DecimalField(Field):  # not in priority
    ...


class DurationField(Field):  # ?????
    ...  # from date time to date time


class EmailField(Field):  # ?????
    ...


class FloatField(Field):
    def edit(self, *, value=empty, obj=empty) -> Control:
        value = self._get_edit_value(value=value, obj=obj)
        return self.edit_widget(value=value)


class IntegerField(Field):
    initial_empty_value = 0
    edit_widget = IntegerInput


class MultipleChoiceField(Field):
    ...


class RegexField(Field):
    ...


class TextField(CharField):
    display_widget = MultiLineTextViewer
    edit_widget = MultiLineTextEditor


class URLField(Field):
    default_validators = [URLValidator]


class MethodField(Field):
    def __init__(self, method: FunctionType, *args, **kwargs):
        self.method: FunctionType = method

        assert kwargs.get('read_only') is not False, (
            'MethodField должно быть только на чтение'
        )

        super().__init__(*args, **kwargs)

    def _get_display_value(self, obj):
        return self.method(obj)

    def _get_db_value(self, obj):
        raise AttributeError(
            'MethodField не обеспечивает функционал получения значений.'
        )

    def get_editing_default_value(self, obj):
        raise AttributeError(
            'MethodField не предоставляет функции редактирования объектов.'
        )

    def _editing_form_widget(self, value, action: str = None):
        raise AttributeError(
            'MethodField не предоставляет функции редактирования объектов.'
        )


class RelatedField(Field):
    # TODO override decorator
    def _get_display_value(self, obj):
        raise AttributeError(
            'отображаемое значение должно быть переопределено в RelatedField'
        )

    def display(self, obj) -> Control:
        raise AttributeError(
            'отображаемое значение должно быть переопределено в RelatedField'
        )


class ForeignKeyField(RelatedField):
    display_widget = ForeignKeyViewer
    edit_widget = ForeignKeyEditor

    def __init__(
        self,
        source: str,
        foreign_form,  # form for getting fields for display object
        # queryset: Callable = None,
        read_only=False,
        write_only=False,
        required: bool = None,
        default=empty,
        label: str = '',
        help_text: str = None,
        style=None,
        error_messages: dict = None,
        validators: list = [],
        allow_null=False,
        # special
    ):
        self.fields = foreign_form()._form_fields(write_only=False).values()
        self.foreign_form = foreign_form
        self.default_validators = [ForeignKeyValidator(foreign_form().Meta.model)]

        # self.queryset = queryset
        # self.default_validators = self.default_validators.copy()
        # self.default_validators.append(
        #     ForeignKeyValidator(foreign_form().Meta.model)
        # )

        super().__init__(
            source=source,
            read_only=read_only,
            write_only=write_only,
            required=required,
            default=default,
            label=label,
            help_text=help_text,
            style=style,
            validators=validators,
            error_messages=error_messages,
            allow_null=allow_null,
        )

    def _get_display_value(self, obj):
        return str(self._get_db_value(obj))

    def display(self, obj) -> Control:
        # TODO mb bullshit
        label = self._get_display_value(obj)
        return self.display_widget(
            obj=self._get_db_value(obj), fields=self.fields, label=label
        )

    def edit(self, *, value=empty, obj=empty) -> Control:
        default_key = self._get_edit_value(value=value, obj=obj)
        if default_key:
            default_key = default_key.id

        return self.edit_widget(
            queryset=self.foreign_form.Meta.model.select,
            default_key=default_key
        )


class StringRelatedField(RelatedField):
    def displayed_value(self):
        return str(self.related_object)


class ManyRelatedField(Field):
    ...
