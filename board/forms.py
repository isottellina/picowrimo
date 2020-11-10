import django_filters
from .models import Advancement

class AdvancementFilter(django_filters.FilterSet):
    start_min = django_filters.DateFilter(field_name='start', lookup_expr='gte')
    start_max = django_filters.DateFilter(field_name='start', lookup_expr='lte')
    end_min = django_filters.DateFilter(field_name='end', lookup_expr='gte')
    end_max = django_filters.DateFilter(field_name='end', lookup_expr='lte')

    class Meta:
        model = Advancement
        fields = ('start_min', 'start_max', 'end_min', 'end_max', )