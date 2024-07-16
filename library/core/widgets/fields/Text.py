from .BaseViewer import Viewer
from library.core.widgets.text import Text
from flet import TextField
from .BaseInput import InputField


class TextViewer(Text, Viewer):
    # TODO init for settings
    "View content as Text."


class TextEditor(TextField, InputField):
    @property
    def clear_value(self) -> str:
        value = super().clear_value
        if value == '':
            return None

        return value


class MultiLineTextEditor(TextField, InputField):
    defaults = {
        'multiline': True,
    }

    def __init__(self, *args, **kwargs):
        kwargs = kwargs | self.defaults
        super().__init__(*args, **kwargs)


class MultiLineTextViewer(Text, Viewer):
    defaults = {
        'width': 270,
    }

    def __init__(self, value, *args, **kwargs):
        kwargs = kwargs | self.defaults
        super().__init__(value, *args, **kwargs)
