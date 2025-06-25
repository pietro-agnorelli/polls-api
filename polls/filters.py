from django_filters import rest_framework as filters
from .models import Polls


class PollsFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    creator__username = filters.CharFilter(lookup_expr='icontains')
    active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Polls
        fields = ['title', 'description', 'creator__username', 'active']