from rest_framework import serializers

from apps.mascotas.models import Mascota


class MacotaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = ['nombre', 'descripcion', 'genero', 'foto', 'en_adopcion']