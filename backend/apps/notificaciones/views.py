from rest_framework.views import APIView, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notificacion
from .serializers import NotificacionModelSerializer



class NotificacionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificacionModelSerializer

    def get_queryset(self):
        usuario = self.request.user
        return Notificacion.objects.filter(destinatario=usuario)
    

class MarcarNotificacionLeidaView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notificacion = Notificacion.objects.get(pk=pk, destinatario=request.user)
        except Notificacion.DoesNotExist:
            return Response(
                {'detail': 'Notificación no encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        notificacion.is_leida = True
        notificacion.save()

        serializer = NotificacionModelSerializer(notificacion)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


############################################################################
################# MALAS PRACTICAS; DEJAR DE EJEMPLO ########################
############################################################################

# class NotificacionesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         notificaciones = Notificacion.objects.filter(destinatario=request.user)
#         serializer = NotificacionModelSerializer(notificaciones, many=True)
#         return Response(serializer.data)

#     def patch(self, request, pk):
#         try:
#             notificacion = Notificacion.objects.get(pk=pk, destinatario=request.user)
#         except Notificacion.DoesNotExist:
#             return Response(
#                 {'detail': 'Notificación no encontrada.'},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         notificacion.is_leida = True
#         notificacion.save()

#         serializer = NotificacionModelSerializer(notificacion)
#         return Response(serializer.data)

