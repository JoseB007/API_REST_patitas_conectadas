from django.db import models
from django.contrib.auth.models import User

from apps.mascotas.models import Mascota

# Create your models here.
class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_like')
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascota_likey')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
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