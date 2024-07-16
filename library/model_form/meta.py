from peewee import Field
from collections import OrderedDict


class UIModelFormMetaClass(type):
    """
    This metaclass sets a dictionary named `_declared_fields` on the class.

    Any instances of `Field` included as attributes on either the class
    or on any of its superclasses will be include in the
    `_declared_fields` dictionary.
    """

    @classmethod
    def _get_declared_fields(cls, bases, attrs):
        fields = [
            (field_name, attrs.pop(field_name))
            for field_name, obj in list(attrs.items())
            if isinstance(obj, Field)
        ]

        return OrderedDict(fields)

    def __new__(cls, name, bases, attrs):
        # attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        return super().__new__(cls, name, bases, attrs)
