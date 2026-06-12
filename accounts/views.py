from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from accounts.models import User
from accounts.serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer


class AuthAPIView(viewsets.GenericViewSet,CreateModelMixin):
     queryset = User.objects.all()
     serializer_class = UserSerializer

     def get_permissions(self):
         if self.action in ('logout', 'session'):
             return [permissions.IsAuthenticated()]
         else:
             return [permissions.AllowAny()]

     @action(methods=['post'], detail=False, url_path='register',serializer_class=UserRegistrationSerializer)
     def register(self, request):
         serializer = UserRegistrationSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
     @action(methods=['get'], detail=False, url_path='login',serializer_class=UserLoginSerializer)
     def login(self, request):
         serializer = UserLoginSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         user = serializer.validated_data['user']
         serializer.save()
         return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

     @action(methods=['delete'], detail=False, url_path='login')
     def logout(self, request):
         logout(request)
         return Response(status=status.HTTP_204_NO_CONTENT)

     @action(methods=['get'], detail=False, url_path='session',serializer_class=UserSerializer)
     def session(self, request):
        user=request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

