class Viewer():
    # todo remove it
    has_value_for_copy = True  # In else don`t copy

    @property
    def copy_value(self):
        return getattr(self, 'value', None)

# TODO rename ~ SeeField? ~ EditField? ~
