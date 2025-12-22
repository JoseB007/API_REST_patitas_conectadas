from django.contrib import admin

from .models import Mascota, Like, RankingMensual


# Register your models here.
admin.site.register(Mascota)
admin.site.register(Like)
admin.site.register(RankingMensual)
