from django_filters import rest_framework as filters

from ..models import Raza


class RazaFilter(filters.FilterSet):
    especie = filters.CharFilter(
        lookup_expr='iexact',
        field_name='especie__slug'
    )

    class Meta:
        model = Raza
        fields = ['especie']