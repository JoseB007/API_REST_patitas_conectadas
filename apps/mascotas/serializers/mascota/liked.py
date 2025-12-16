from rest_framework import serializers

from ...models import Like


class LikeModelSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    mascota = serializers.ReadOnlyField(source='mascota.nombre')
    f_creacion = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )

    class Meta:
        model = Like
        fields = ['id', 'usuario', 'mascota', 'f_creacion']