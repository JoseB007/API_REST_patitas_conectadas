from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lectura permitida para cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        # Escritura solo para el dueño
        return obj.usuario == request.user
