from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)


from .models import Mascota
from .serializers import (
    MascotaListSerializer, 
    MascotaDetailSerializer, 
    MacotaCreateUpdateSerializer,
    LikeModelSerializer,
)
from .permissions import IsOwnerOrAdminOrReadOnly
from .models import Like



from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_root(request, format=None):
    """
    API endpoints raíz
    """
    return Response({
        'usuarios': reverse('usuario-list', request=request, format=format),
        'mascotas': reverse('mascota-list', request=request, format=format),
        'adopciones': reverse('adopcion-list', request=request, format=format),
        'likes': reverse('like-list', request=request, format=format),
    })


class BaseViewSet(viewsets.ModelViewSet):
    queryset = None
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

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
    
    @action(detail=True, methods=['post'], url_path='toggle-like', permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        mascota = self.get_object()
        usuario = request.user

        like_user = Like.objects.filter(usuario=usuario, mascota=mascota)
        if like_user.exists():
            like_user.delete()
            return Response({'Liked': False})
        else:
            Like.objects.create(usuario=usuario, mascota=mascota)
            return Response({
                'Liked': True,
                'msj': "Indicaste que te gusta este amiguito!"
            })


class AdopcionesViewSet(BaseViewSet):
    queryset = Mascota.objects.filter(en_adopcion=True)


class LikedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeModelSerializer

