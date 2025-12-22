from django.urls import path

from . import views

urlpatterns = [
    path("notificaciones/", views.NotificacionListView.as_view(), name="notificaiones"),
    path("notificaciones/<int:pk>/leer/", views.MarcarNotificacionLeidaView.as_view(), name="notificacion-leer"),
]