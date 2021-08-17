from rest_framework import viewsets


class ModelViewSet(viewsets.ModelViewSet):
    """
    Generic model viewset.
    Serializer_class attribute is required.

    Sensible defaults include:
        - model
        - queryset
    """

    def get_model(self):
        """
        Default model is inherited from the serializer.
        """
        return self.serializer_class.Meta.model

    def get_queryset(self):
        """
        Return all objects by default.
        """
        return self.get_model().objects.all()
