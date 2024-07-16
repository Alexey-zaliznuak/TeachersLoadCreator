from typing import Generic, TypeVar
from functools import partial


Attribute = TypeVar('Attribute')


class LazyAttribute(Generic[Attribute]):
    def __init__(
        self,
        obj,
        attr: str,
        args: tuple = (),
        kwargs: dict = {},
        *,
        attrs_separator: str = '.',
        return_partial: bool = True,
    ):
        self.obj = obj
        self.full_attr = attr

        self.attrs_separator = attrs_separator
        self.return_partial = return_partial

        self.args = args
        self.kwargs = kwargs

    def __call__(self) -> Attribute:
        full_attr = self.full_attr
        primitive_attr = full_attr.split(self.attrs_separator)[0]

        attr = getattr(self.obj, primitive_attr)

        while self.attrs_separator in full_attr:
            full_attr = full_attr.removeprefix(
                primitive_attr + self.attrs_separator
            )

            primitive_attr = full_attr.split(self.attrs_separator)[0]
            attr = getattr(attr, primitive_attr)

        if callable(attr):
            part = partial(attr, *self.args, **self.kwargs)

            if self.return_partial:
                return part

            return part()

        return attr
