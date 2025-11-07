from rest_framework import serializers

from django.contrib.auth.models import User

from apps.mascotas.serializers import MascotaListSerializer


class UserDetailSerializer(serializers.ModelSerializer):
    mascotas = MascotaListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mascotas']


class AdminUserDetailSerializer(serializers.ModelSerializer):
    # mascotas = MascotaListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']