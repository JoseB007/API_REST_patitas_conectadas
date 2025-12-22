from rest_framework import serializers

from apps.mascotas.models import Mascota, Especie, Raza


class MacotaCreateUpdateSerializer(serializers.ModelSerializer):
    especie = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Especie.objects.all(),
        required=False,
        allow_null=True
    )
    raza = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Raza.objects.all(),
        required=False,
        allow_null=True
    )

    foto = serializers.ImageField(
        required=False,
        allow_null=True,
        use_url=True
    )

    class Meta:
        model = Mascota
        fields = ['nombre', 'descripcion', 'genero', 'foto', 'especie', 'raza', 'en_adopcion']

    def validate_foto(self, value):
        """
        Validar tamaño y tipo de archivo.
        """
        if value:
            # ▼ 1) Validar tamaño (ej: máximo 3 MB)
            max_size = 3 * 1024 * 1024  # 3 MB
            if value.size > max_size:
                raise serializers.ValidationError("La imagen debe pesar menos de 3 MB.")

            # ▼ 2) Validar tipo MIME
            valid_types = ['image/jpeg', 'image/png', 'image/webp']
            if value.content_type not in valid_types:
                raise serializers.ValidationError("Formato no permitido. Usa JPG, PNG o WEBP.")

        return value
    
    # def create(self, validated_data):
    #     """
    #     Asociar la mascota al usuario autenticado.
    #     """
    #     usuario = self.context['request'].user
    #     return Mascota.objects.create(usuario=usuario, **validated_data)
    
    def update(self, instance, validated_data):
        """
        Permitir reemplazar la foto o mantener la anterior.
        """
        foto = validated_data.get('foto', None)

        if foto is None and self.partial:
            validated_data['foto'] = instance.foto

        return super().update(instance, validated_data)