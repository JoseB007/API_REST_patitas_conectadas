from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Mascota, Like


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'mascotas', 'usuario_like']


# Serializer resumido para listas
class MascotaListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mascota
        fields = ['url', 'id', 'nombre', 'genero', 'foto']


# Serializer detallado
class MascotaDetailSerializer(serializers.HyperlinkedModelSerializer):
    usuario = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    likes = UserListSerializer(many=True, read_only=True)  # O simplemente IDs

    class Meta:
        model = Mascota
        fields = ['url', 'id', 'usuario', 'nombre', 'descripcion', 'genero', 'foto', 'en_adopcion', 'likes', 'fecha']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'usuario', 'mascota', 'fecha']











# class UserSerializer(serializers.ModelSerializer):
#     mascotas = serializers.PrimaryKeyRelatedField(many=True, queryset=Mascota.objects.all())

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_superuser', 'mascotas']



# class MascotaSerializer(serializers.ModelSerializer):
#     usuario = serializers.ReadOnlyField(source='usuario.username')

#     class Meta:
#         model = Mascota
#         fields = ['id', 'usuario', 'nombre', 'descripcion', 'genero', 'foto', 'fecha']



# class MascotaSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     usuario = serializers.ReadOnlyField(source='usuario.username')
#     nombre = serializers.CharField()
#     descripcion = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
#     genero = serializers.ChoiceField(choices=Mascota.GENERO)
#     foto = serializers.FileField(required=False)
#     fecha = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Mascota.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.nombre = validated_data.get('nombre', instance.nombre)
#         instance.descripcion = validated_data.get('descripcion', instance.descripcion)
#         instance.genero = validated_data.get('genero', instance.genero)
#         instance.foto = validated_data.get('foto', instance.foto)
#         instance.usuario = validated_data.get('usuario', instance.usuario)
#         instance.save()
#         return instance