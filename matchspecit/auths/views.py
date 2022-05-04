from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from matchspecit.auths.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
)
from matchspecit.core import settings


class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    merge_data = {
        'user': "user"
    }
    html_body = render_to_string("email/register_email_confirmation.html", merge_data)
    message = EmailMultiAlternatives(
       subject='Django HTML Email',
       from_email=settings.EMAIL_HOST_USER,
       to=[settings.EMAIL_HOST]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
