from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Like
from .serializers import LikeListSerializer, LikeCreateSerializer, LikeUpdateSerializer
from .permissions import IsOwnerOrReadOnly

from apps.mascotas.models import Mascota


# Create your views here.
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return LikeListSerializer
        elif self.action in ['update', 'partial_update']:
            return LikeUpdateSerializer
        return LikeCreateSerializer

    def create(self, request, *args, **kwargs):
        usuario = request.user
        mascota_id = request.data.get('mascota')

        if not mascota_id:
            return Response({'error': 'ID de mascota requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mascota = Mascota.objects.get(pk=mascota_id)
        except Mascota.DoesNotExist:
            return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(usuario=usuario, mascota=mascota)

        if like.exists():
            like.delete()
            return Response({'liked': False}, status=status.HTTP_200_OK)
        else:
            new_like = Like.objects.create(usuario=usuario, mascota=mascota)
            serializer = LikeListSerializer(new_like)
            return Response({'liked': True, 'like': serializer.data}, status=status.HTTP_201_CREATED)

