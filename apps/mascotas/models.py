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
    likes = models.ManyToManyField(User, through='likes.Like', related_name='mascota_likes')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'

    def __str__(self):
        return f"{self.nombre}, Amiguito de {self.usuario.username}"
    
    def get_foto(self):
        if self.foto:
            return self.foto.url
        return "/static/img/pets.svg"