import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Mascota(models.Model):
    MACHO = "Macho"
    HEMBRA = "Hembra"
    GENERO = [
        (MACHO, "Macho"),
        (HEMBRA, "Hembra")
    ]
    usuario = models.ForeignKey('auth.User', related_name='mascotas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True, null=True)
    genero = models.CharField(max_length=6, choices=GENERO, default=MACHO)
    foto = models.FileField(upload_to='mascotas/fotos/', blank=True, null=True)
    en_adopcion = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_mascotas')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    f_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-f_creacion']
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'

    def __str__(self):
        return f"{self.nombre}, Amiguito de {self.usuario.username}"
    
    def get_foto(self):
        if self.foto:
            return self.foto.url
        return "/static/img/pets.svg"    


class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_mascota')
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='likes_mascota')
    f_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-f_creacion']
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'mascota'],
                name='unique_like'
            )
        ]

    def __str__(self):
        return f"{self.usuario.username} ha dado like a {self.mascota.nombre}"


