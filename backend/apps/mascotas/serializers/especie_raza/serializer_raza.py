from rest_framework import serializers

from ...models import Raza, Especie


class RazaModelSerializer(serializers.ModelSerializer):
    especie = serializers.ReadOnlyField(source='especie.nombre')

    class Meta:
        model = Raza
        fields = ['nombre', 'slug', 'especie']


class RazaCreateUpdateSerializer(serializers.ModelSerializer):
    especie = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Especie.objects.all()
    )

    class Meta:
        model = Raza
        fields = ['nombre', 'especie']
