from django.urls import path

from matchspecit.technology.views import TechnologyView

urlpatterns = [
    path("technology/", TechnologyView.as_view(), name="technology_view"),
]
