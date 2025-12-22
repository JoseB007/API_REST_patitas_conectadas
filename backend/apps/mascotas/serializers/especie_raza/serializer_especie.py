from rest_framework import serializers

from ...models import Especie


class EspecieModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = ['nombre', 'slug']