from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """El dueño o el admin puede editar el objeto"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user