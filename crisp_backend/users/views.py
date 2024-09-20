from django.shortcuts import render
from rest_framework import generics, status
from .serializers import CitizenSerializer, LoginSerializer, WorkersSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response

class CitizenRegisterView(generics.CreateAPIView):
    serializer_class = CitizenSerializer

class WorkersRegisterView(generics.CreateAPIView):
    serializer_class = WorkersSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
