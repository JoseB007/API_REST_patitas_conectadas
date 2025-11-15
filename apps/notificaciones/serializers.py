from rest_framework import serializers

from .models import Notificacion


class NotificacionModelSerializer(serializers.ModelSerializer):
    destinatario = serializers.CharField(source='destinatario.username', read_only=True)
    autor = serializers.CharField(source='autor.username', read_only=True)
    f_creacion = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Notificacion
        fields = ['destinatario', 'autor', 'descripcion', 'is_leida', 'f_creacion']
        read_only_fields = ['destinatario', 'autor', 'descripcion', 'f_creacion']
