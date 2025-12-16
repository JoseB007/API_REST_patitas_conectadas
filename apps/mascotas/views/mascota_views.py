from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from ..models import Mascota, Like
from ..utils.permissions import IsOwnerOrAdminOrReadOnly
from ..filters.mascotas_filters import MascotaFilter
from ..serializers import (
    MascotaListSerializer, 
    MascotaDetailSerializer, 
    MacotaCreateUpdateSerializer,
    LikeModelSerializer,
)

from ..services.mascotas_ranking import RankingService

from ..utils.timezone import (
    get_today,
    get_yesterday,
    get_last_week_range
)

from django_filters import rest_framework as filters

from django.db.models import Count


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
    """
    ViewSet para todas las operaciones CRUD de Mascota.
    - Usa `lookup_field = 'uuid'`
    - Selecciona serializer según la acción.
    - Permite subir imágenes al crear o editar.
    """

    queryset = None
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]
    lookup_field = 'uuid'

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MascotaFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MascotaDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MacotaCreateUpdateSerializer
        return MascotaListSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class MascotasViewSet(BaseViewSet):
    queryset = queryset = Mascota.objects.filter(
        en_adopcion=False
    ).annotate(
        likes_count=Count('likes')
    )

    @action(detail=True, methods=['post'], url_path='toggle-like', permission_classes=[IsAuthenticated])
    def toggle_like(self, request, **kwargs):
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

    
class MascotasRankingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        rango = request.query_params.get("rango", "global")

        hoy = get_today()
        ayer = get_yesterday()
        inicio, fin = get_last_week_range()

        manejadores = {
            "global": lambda: RankingService.top_global(),
            "hoy": lambda: RankingService.top_por_fecha(hoy),
            "ayer": lambda: RankingService.top_por_fecha(ayer),
            "semana_pasada": lambda: RankingService.top_por_rango(inicio, fin)
        }

        if rango not in manejadores:
            return Response({
                'error': 'Parámetro "rango" inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        resultado = manejadores[rango]()
        many = isinstance(resultado, list) or hasattr(resultado, "__iter__")

        serializer = MascotaDetailSerializer(
            resultado,
            many=many,
            context={'request': request}
        )

        return Response({
            "rango": rango,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
