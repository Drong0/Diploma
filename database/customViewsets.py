from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet


class ModelViewSetWithoutRetrieve(mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.ListModelMixin,
                                  GenericViewSet):
    """
    A viewset that provides default `create()` `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
