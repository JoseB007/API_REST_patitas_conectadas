from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)

from ..models import Especie, Raza
from ..serializers import EspecieModelSerializer, RazaModelSerializer, RazaCreateUpdateSerializer
from ..filters.razas_filters import RazaFilter

from django_filters import rest_framework as filters


class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.all()
    serializer_class = EspecieModelSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        public_actions = ['list', 'retrieve']
        private_actions = ['create', 'update', 'partial_update', 'destroy']

        if self.action in public_actions:
            permission_classes = [AllowAny]
        elif self.action in private_actions:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class RazaViewSet(viewsets.ModelViewSet):
    queryset = Raza.objects.all()
    lookup_field = 'slug'

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RazaFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RazaCreateUpdateSerializer
        return RazaModelSerializer
    
    def get_permissions(self):
        public_actions = ['list', 'retrieve']
        private_actions = ['create', 'update', 'partial_update', 'destroy']

        if self.action in public_actions:
            permission_classes = [AllowAny]
        elif self.action in private_actions:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    # @action(detail=False, methods=['get'], url_path='por-especie')
    # def por_especie(self, request):
    #     data = []

    #     especies = Especie.objects.prefetch_related('razas')

    #     for especie in especies:
    #         data.append({
    #             'especie': especie.nombre,
    #             'slug': especie.slug,
    #             'razas': [
    #                 {'nombre': r.nombre, 'slug': r.slug}
    #                 for r in especie.razas.all()
    #             ]
    #         })

    #     return Response(data, status=status.HTTP_200_OK)