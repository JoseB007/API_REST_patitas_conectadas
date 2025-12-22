from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'usuarios', views.UserViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    path('mi-perfil/', views.MiPerfilView.as_view(), name='mi-perfil'),
]