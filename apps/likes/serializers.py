from rest_framework import serializers

from .models import Like

class LikeListSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    mascota = serializers.ReadOnlyField(source='mascota.nombre')

    class Meta:
        model = Like
        fields = ['id', 'usuario', 'mascota', 'fecha']


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['usuario', 'mascota']


class LikeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['mascota']

    def update(self, instance, validated_data): 
        usuario = instance.usuario  # el usuario ya está asignado
        nueva_mascota = validated_data.get('mascota')

        # Verifica si ya existe un Like con esa combinación
        if Like.objects.exclude(pk=instance.pk).filter(usuario=usuario, mascota=nueva_mascota).exists():
            raise serializers.ValidationError("Ya hiciste like a esta mascota.")

        return super().update(instance, validated_data)


