from django.contrib import admin
from django.db import models

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
        return [
            field.name for field in self.get_model_fields()
            if any(isinstance(field, x) for x in [
                models.fields.BooleanField,
                models.ForeignKey,
                models.ManyToManyField
            ]) and field.unique is False
        ]

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
                if isinstance(field, models.fields.BooleanField)]

    def get_changelist_instance(self, request):
        """
        Override admin method for dynamic list_editable.
        """
        self.list_editable = self.get_list_editable(request)

        return super().get_changelist_instance(request)
