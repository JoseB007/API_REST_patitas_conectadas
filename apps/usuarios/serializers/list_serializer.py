from rest_framework import serializers

from django.contrib.auth.models import User


class UserListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='usuario-detail')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email']

