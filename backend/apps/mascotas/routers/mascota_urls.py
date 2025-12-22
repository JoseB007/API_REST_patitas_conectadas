from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.mascotas.views import mascota_views


router = DefaultRouter()
router.register(r'mascotas', mascota_views.MascotasViewSet, basename='mascota')
router.register(r'adopciones', mascota_views.AdopcionesViewSet, basename='adopcion')
router.register(r'likes', mascota_views.LikedViewSet, basename='like')

urlpatterns = [
    path('', mascota_views.api_root),
    path('', include(router.urls)),
    path('ranking/', mascota_views.MascotasRankingView.as_view(), name='ranking'),
]