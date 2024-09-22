from django.shortcuts import render
from rest_framework import generics, status
from .serializers import CitizenSerializer, WorkersSerializer, DepartmentHeadSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


class CitizenRegisterView(generics.CreateAPIView):
    serializer_class = CitizenSerializer
    permission_classes = [AllowAny]

class WorkersRegisterView(generics.CreateAPIView):
    serializer_class = WorkersSerializer
    permission_classes = [AllowAny]

class DepartmentHeadRegisterView(generics.CreateAPIView):
    serializer_class = DepartmentHeadSerializer
    permission_classes = [AllowAny]

class ProtectedView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a protected view.'})

class HealthView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'message': 'This is a for health check.'})

    
