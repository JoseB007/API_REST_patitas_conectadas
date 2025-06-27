from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Mascota
from .serializers import MascotaSerializer


@api_view(['GET', 'POST'])
def mascota_list(request, format=None):
    if request.method == 'GET':
        mascotas = Mascota.objects.all()
        serializer = MascotaSerializer(mascotas, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'detalle': 'Autenticación requerida'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])    
def mascota_detail(request, pk, format=None):
    try:
        mascota = Mascota.objects.get(pk=pk)
    except Mascota.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)
    
    if request.method in ['PUT', 'DELETE']:
        if not request.user.is_authenticated:
            return Response({'detail': 'Autenticación requerida'}, status=status.HTTP_401_UNAUTHORIZED)

        if mascota.usuario != request.user:
            return Response({'detail': 'No tienes permiso para modificar esta mascota.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = MascotaSerializer(mascota, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        mascota.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)