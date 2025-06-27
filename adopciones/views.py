from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .import serializers
from .models import Mascota, Like
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserListSerializer


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MascotaListSerializer
        return serializers.MascotaDetailSerializer

    # @action(detail=False, methods=['get'], url_path="mis-mascotas", permission_classes=[permissions.IsAuthenticated])
    # def mis_mascotas(self, request):
    #     mascotas = self.queryset.filter(usuario=request.user)
    #     serializer = self.get_serializer(mascotas, many=True)
    #     return Response(serializer.data)
    
    # @action(detail=False, methods=['get'])
    # def buscar(self, request):
    #     termino = request.GET.get('ref', '')
    #     mascotas = self.queryset.filter(nombre__icontains=termino)
    #     serializer = self.get_serializer(mascotas, many=True)
    #     return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


