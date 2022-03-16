from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from matchspecit.auths.views import ObtainTokenPairView, RegisterView

urlpatterns = [
    path("login/", ObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path(r"password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
]
