from django.db.models import Q
import django_filters
from .models import User


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = User
        fields = []

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )
