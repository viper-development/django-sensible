from django.contrib import admin
from django.db import models


def is_field_choice_input(field):
    """
    Return if a field is a CharField with enforced choice input.
    """
    return isinstance(field, models.CharField) and field.choices


def is_field_filter(field):
    """
    Return true if a field is suitable for filtering in display list.
    """
    valid_models = [
        models.fields.BooleanField,
        models.ForeignKey,
        models.ManyToManyField
    ]

    # Choice fields can be used as a filter
    # (There is a limited number of possible values).
    return (any(isinstance(field, model) for model in valid_models)
            or is_field_choice_input(field))


def is_field_editable(field):
    """
    Return true if a field is suitable for edition in display list
    (Essentially boolean fields, thanks for their tiny widget).
    """
    return (is_field_choice_input(field)
            or isinstance(field, models.BooleanField))


class ModelAdmin(admin.ModelAdmin):
    """
    Generic ModelAdmin with shortcuts.
    Automatic generation editable fields for:
        - BooleanField
    """

    def get_model_fields(self):
        return self.model._meta.fields

    def get_list_filter(self, request):
        """
        Build a list of filters, composed of relationnal and boolean fields.
        """
        return [field.name for field in self.get_model_fields()
                if is_field_filter(field)]

    def get_list_display(self, request):
        """
        Display the list of filters + the tostring representation
        """
        return ['__str__'] + self.get_list_filter(request)

    def get_list_editable(self, request):
        """
        From the list display, those fields can be edited and saved.
        """
        return [field.name for field in self.get_model_fields()
                if is_field_editable(field)]

    def get_changelist_instance(self, request):
        """
        Override admin method for dynamic list_editable.
        """
        self.list_editable = self.get_list_editable(request)

        return super().get_changelist_instance(request)
