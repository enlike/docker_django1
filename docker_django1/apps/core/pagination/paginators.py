import inspect

from django.core.paginator import Paginator
from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args
from rest_framework.pagination import PageNumberPagination


class FasterDjangoPaginator(Paginator):
    @cached_property
    def count(self):
        c = getattr(self.object_list, 'count', None)
        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            # only select 'id' for counting, much cheaper
            return self.object_list.values('id').count()
        return len(self.object_list)


class FasterPageNumberPagination(PageNumberPagination):
    page_size = 25
    django_paginator_class = FasterDjangoPaginator
