from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import ChoiceField


class EnumField(ChoiceField):
    default_error_messages = {
        'invalid': _("No matching enum type.")
    }

    def __init__(self, **kwargs):
        self.enum_type = kwargs.pop("enum_type")
        kwargs.pop("choices", None)
        super(EnumField, self).__init__(self.enum_type.choices(), **kwargs)

    def to_internal_value(self, data):
        for choice in self.enum_type:
            if choice.name == data or choice.value == data:
                return choice
        self.fail("invalid")

    def to_representation(self, value):
        # this can be either an enum member or a "choice", i.e. a str
        if hasattr(value, "value"):
            return value.value
        return value
