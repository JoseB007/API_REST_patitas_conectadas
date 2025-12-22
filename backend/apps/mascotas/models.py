import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Especie(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique=True, 
        blank=True, null=True, help_text="Slug de la especie",
    )

    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)

        super().save(*args, **kwargs)


class Raza(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="razas")
    slug = models.SlugField(
        max_length=100, unique=True,
        blank=True, null=True, help_text="Slug de la raza",
    )

    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)

        super().save(*args, **kwargs)


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
    especie = models.ForeignKey(Especie, on_delete=models.SET_NULL, blank=True, null=True, related_name='mascotas')
    raza = models.ForeignKey(Raza, on_delete=models.SET_NULL, blank=True, null=True, related_name='mascotas')
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


class RankingMensual(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='ganadora_mes')
    mes = models.PositiveSmallIntegerField()
    anio = models.PositiveSmallIntegerField()
    total_likes = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Ranking Mensual"
        verbose_name_plural = "Ranking Mensual"
        ordering = ["-anio", "-mes"]
        UniqueConstraint(
            fields=['mes', 'anio'], 
            name="mascota_mes_anio"
        )
