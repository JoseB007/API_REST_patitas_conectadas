from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'mascotas', views.MascotasViewSet, basename='mascota')
router.register(r'adopciones', views.AdopcionesViewSet, basename='adopcion')
router.register(r'likes', views.LikedViewSet, basename='like')

urlpatterns = [
    path('', views.api_root),
    path('', include(router.urls)),
]