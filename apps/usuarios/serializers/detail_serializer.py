from rest_framework import serializers

from django.contrib.auth.models import User

from apps.mascotas.serializers import MascotaListSerializer


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    mascotas = MascotaListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'mascotas']