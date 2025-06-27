from rest_framework import serializers

from apps.mascotas.models import Mascota
from apps.usuarios.serializers import UserListSerializer


class MascotaDetailSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    usuario = UserListSerializer(read_only=True)

    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'descripcion', 'genero', 'foto_url', 'en_adopcion', 'likes', 'fecha', 'usuario']

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            return request.build_absolute_uri(obj.foto.url)
        return request.build_absolute_uri('/static/img/pets.svg')