from django_filters import rest_framework as filters

from ..models import Mascota

class MascotaFilter(filters.FilterSet):
    nombre = filters.CharFilter(
        field_name="nombre", 
        lookup_expr='icontains'
    )

    class Meta:
        model = Mascota
        fields = ['nombre', 'genero']