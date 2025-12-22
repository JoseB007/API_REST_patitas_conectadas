from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.mascotas.views import especie_raza_views


router = DefaultRouter()
router.register(r'especies', especie_raza_views.EspecieViewSet, basename='especie')
router.register(r'razas', especie_raza_views.RazaViewSet, basename='raza')

urlpatterns = [
    path('', include(router.urls))
]