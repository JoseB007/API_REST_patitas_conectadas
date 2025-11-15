from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from django.contrib.auth.models import User

from .serializers import (
    UserListSerializer, 
    UserDetailSerializer, 
    UserUpdateSerializer,
    UserCreateSerializer,
    AdminUserListSerializer,
    AdminUserDetailSerializer,
    MyTokenObtainPairSerializer,
)

from core.utils.permissions import IsSelfOrAdmin
from apps.notificaciones.models import Notificacion
from apps.notificaciones.serializers import NotificacionModelSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return AdminUserDetailSerializer if self.request.user.is_superuser else UserDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return AdminUserListSerializer if self.request.user.is_superuser else UserListSerializer
    
    def get_permissions(self):
        public_actions = ['create', 'list', 'retrieve']
        owner_actions = ['update', 'partial_update', 'destroy']

        if self.action in public_actions:
            permission_classes = [AllowAny]
        elif self.action in owner_actions:
            permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path="mi-perfil")
    def mi_perfil(self, request):
        serializer = UserDetailSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    ############################################################################
    ################# MALAS PRACTICAS; DEJAR DE EJEMPLO ########################
    ############################################################################
    
    # @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    # def notificaciones(self, request):
    #     notificaciones_usuario = Notificacion.objects.filter(destinatario=request.user)
    #     serializer = NotificacionModelSerializer(notificaciones_usuario, many=True)
    #     return Response(serializer.data)


class MiPerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserDetailSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, format=None):
        serializer = UserUpdateSerializer(request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
