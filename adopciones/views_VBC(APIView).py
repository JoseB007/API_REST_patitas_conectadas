from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Mascota
from .serializers import MascotaSerializer


class MascotaListView(APIView):
    def get(self, request, format=None):
        mascotas = Mascota.objects.all()
        serializer = MascotaSerializer(mascotas, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MascotaDetailView(APIView):
    def get_object(self, pk):
        try:
            return Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        mascota = self.get_object(pk)
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        mascota = self.get_object(pk)
        serializer = MascotaSerializer(mascota, data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        mascota = self.get_object(pk)
        mascota.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)