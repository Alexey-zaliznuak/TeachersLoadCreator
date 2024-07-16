from library.model_form.filters import (
    FilterSet,
    FieldValueFilter
)
from models import Nickname


class NicknamesFilterSet(FilterSet):
    person = FieldValueFilter(field=Nickname.person)

    class Meta:
        filters = ('person', )
