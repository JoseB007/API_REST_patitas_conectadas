from rest_framework import viewsets, permissions

from .models import Like
from .serializers import LikeListSerializer, LikeCreateSerializer, LikeUpdateSerializer
from .permissions import IsOwnerOrReadOnly

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

