from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mascotas', views.MascotasViewSet, basename='mascotas')
router.register(r'adopciones', views.AdopcionesViewSet, basename='adopciones')

urlpatterns = [
    path('', include(router.urls))
]