from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Like

from apps.notificaciones.models import Notificacion


@receiver(post_save, sender=Like)
def crear_notificacion(sender, instance, created, **kwargs):
    like = instance
    destinatario = like.mascota.usuario
    autor = like.usuario

    if created and destinatario != autor:
        descripcion = f"{autor.username} ha reaccionado a tu mascota: {like.mascota.nombre}"
        
        Notificacion.objects.create(
            destinatario=destinatario,
            autor=autor,
            descripcion=descripcion,
        )
