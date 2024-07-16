from library.model_form import UIModelForm
from library.model_form.fields import ForeignKeyField
from library.model_form.actions.objects import (
    CreateForeignObjectAction,
    DeleteObjectAction,
    DetailObjectAction,
    EditObjectAction,
    SetValueObjectAction,
)
from library.model_form.actions.table import CreateObjectAction

from models import (
    Person,
    Nickname,
)


RUDActions = [
    EditObjectAction(),
    DetailObjectAction(),
    DeleteObjectAction(),
]


class PersonsForm(UIModelForm):
    class Meta:
        model = Person
        fields = ('id', 'name',)
        objects_actions = RUDActions
        table_actions = (CreateObjectAction, )


class NicknamesForm(UIModelForm):
    person = ForeignKeyField('person', PersonsForm)

    class Meta:
        model = Nickname
        fields = ('id', 'name', 'person')
        objects_actions = RUDActions

        table_actions = (CreateObjectAction, )
