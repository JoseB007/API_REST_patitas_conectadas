from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.mascotas.models import Mascota
from apps.usuarios.serializers import UserDetailSerializer


class MascotaListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    foto_url = serializers.SerializerMethodField()
    usuario = UserDetailSerializer(read_only=True)
    f_creacion = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    
    class Meta:
        model = Mascota
        fields = ['url', 'id', 'nombre', 'descripcion', 'genero', 'foto_url', 'en_adopcion', 'likes', 'f_creacion', 'usuario']

    def get_url(self, obj):
        """
        Devuelve la URL detallada dependiendo si la mascota está en adopción o no.
        """
        request = self.context.get('request')
        if obj.en_adopcion:
            return reverse('adopcion-detail', args=[obj.pk], request=request)
        return reverse('mascota-detail', args=[obj.pk], request=request)
    
    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            return request.build_absolute_uri(obj.foto.url)
        return request.build_absolute_uri('/static/img/pets.svg')
    




