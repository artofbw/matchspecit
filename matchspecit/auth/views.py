from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from matchspecit.auth.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
)


class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
