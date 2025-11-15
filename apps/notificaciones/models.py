# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notificacion(models.Model):
    destinatario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notificaciones_recividas"
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notificaciones_enviadas"
    )
    descripcion = models.TextField(max_length=255)
    is_leida = models.BooleanField(default=False)
    f_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-f_creacion']

    def __str__(self):
        return f"Notificación para {self.destinatario} — {self.descripcion[:40]}"
