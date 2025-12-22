from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    # Mascotas
    path("mascotas/", views.MascotaListView.as_view(), name='lista_mascotas'),
    path("mascotas/<int:pk>/", views.MascotaDetailView.as_view(), name='mascota-detail'),
    # Usuarios
    path("usuarios/", views.UserList.as_view(), name='lista_usuarios'),
    path("usuarios/<int:pk>", views.UserDetail.as_view(), name='user-detail'),
    # Raíz API
    path('', views.api_root),
])