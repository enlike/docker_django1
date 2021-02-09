import django_filters

from docker_django1.apps.user.models import User


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    last_name = django_filters.CharFilter(
        field_name='last_name', lookup_expr='icontains'
    )
    first_name = django_filters.CharFilter(
        field_name='first_name', lookup_expr='icontains'
    )
    middle_name = django_filters.CharFilter(
        field_name='middle_name', lookup_expr='icontains'
    )

    class Meta:
        model = User
        exclude = ('is_active',)
