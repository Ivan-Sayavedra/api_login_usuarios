from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers, models, permissions


# APIView de prueba
class HelloApiView(APIView):
    
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        # Retornar lista de caracterísitcas del apiview
        an_apiview = [
            'Usamos métodos HTTP como funciones (get, post)',
            'Es similar a una vista tradicional de django',
            'Nos da el mayor control sobre la logica de nuestra aplicacion',
            'Está mapeado manualmente a los URL'
        ]
        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    # Creo un mensaje con nuestro nombre
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message=f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Para actualizar objeto
    def put(self,request,pk=None):
        return Response({'method': 'PUT'})
    
    # Para actualización parcial del objeto
    def patch(self,request,pk=None):
        return Response({'method':'PATCH'})
    
    def delete(self,request,pk=None):
        return Response({'method':'DELETE'})
    

"""Test de ViewSet"""
 
class HelloViewSet(viewsets.ViewSet):
    
    serializer_class = serializers.HelloSerializer
    
    # Retornar un mensaje
    def list(self, request):
        a_viewset = [
            'Usa acciones (list, create, retrieve, update, partial_update',
            'Automáticamente mapea a los URLs usando Routers',
            'Provee más funcionalidad con menos código'
        ]
        
        return Response({'message':'Holaaa', 'a_viewset': a_viewset})
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Holaaaa {name}'
            return Response(
                {'message': message}
            )
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
     
    # Obtiene un objeto y su id       
    def retrieve(self, request, pk=None):
        return Response({'http_method':'GET'})
    
    def update(self, request, pk=None):
        return Response({'http_method':'PUT'})
    
    def partial_update(self, request, pk=None):
        return Response({'http_method':'PATCH'})
    
    def destroy(self, request, pk=None):
        return Response({'http_method':'DELETE'})

""" Crear y actualizar perfiles """
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)
    
""" Crear token de autenticación de usuario """
class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
""" Maneja el crear, leer y actualizar el profile feed """
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
        )
    
    # Setear el perfil de usuario para el usuario que está logeado
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)