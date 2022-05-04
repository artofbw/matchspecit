from django.urls import path

from matchspecit.user.views import UserView

urlpatterns = [
    path("user/", UserView.as_view(), name="user_technologies_view"),
]
