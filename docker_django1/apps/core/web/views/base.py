from typing import Tuple

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


class BaseView(viewsets.ModelViewSet):
    """
    Base DRF ModelViewSet
    :argument filterset_class - inherited by django_filters
    :argument serializer_class - serializer_class
    :argument order_args - tuple to order your QS
    """

    filter_backends = (DjangoFilterBackend,)
    filterset_class = None
    serializer_class = None
    order_args: Tuple = tuple

    def get_queryset(self):
        assert self.filterset_class, 'Enter filterset_class!'
        assert self.serializer_class, 'Enter serializer_class!'
        model = self.get_serializer_class().Meta.model
        if self.order_args:
            return model.objects.order_by(*self.order_args)
        else:
            return model.objects.all()
