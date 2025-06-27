from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Mascota
from .serializers import MascotaListSerializer, MascotaDetailSerializer, MacotaCreateUpdateSerializer
from .permissions import IsOwnerOrReadOnly

from apps.likes.models import Like


# Create your views here.
class BaseViewSet(viewsets.ModelViewSet):
    queryset = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MascotaDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MacotaCreateUpdateSerializer
        return MascotaListSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)



class MascotasViewSet(BaseViewSet):
    queryset = Mascota.objects.filter(en_adopcion=False)
    
    @action(detail=True, methods=['post'], url_path='toggle-like', permission_classes=[permissions.IsAuthenticated])
    def toggle_like(self, request, pk=None):
        mascota = self.get_object()
        usuario = request.user

        like_user = Like.objects.filter(usuario=usuario, mascota=mascota)
        if like_user.exists():
            like_user.delete()
            return Response({'Liked': False})
        else:
            Like.objects.create(usuario=usuario, mascota=mascota)
            return Response({'Liked': True})



class AdopcionesViewSet(BaseViewSet):
    queryset = Mascota.objects.filter(en_adopcion=True)

