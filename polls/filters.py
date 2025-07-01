from django_filters import rest_framework as filters
from .models import Polls#, Choices


class PollsFilter(filters.FilterSet):


    class Meta:
        model = Polls
        fields = ['id']



"""
class ChoicesFilter(filters.FilterSet):
    choice_text = filters.CharFilter(lookup_expr='icontains')
    poll__title = filters.CharFilter(field_name='poll__title', lookup_expr='icontains')

    class Meta:
        model = Choices
        fields = ['poll__title']  # Assuming Choice model has a ForeignKey to Polls
"""