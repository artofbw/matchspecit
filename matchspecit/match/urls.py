from django.urls import path

from matchspecit.match.views import (
    MatchDetail,
    MatchProjectMatchedView,
    MatchProjectView,
    MatchSpecialistMatchedView,
    MatchSpecialistView,
)

urlpatterns = [
    path("match/specialist/", MatchSpecialistView.as_view(), name="match_view"),
    path("match/specialist/matched", MatchSpecialistMatchedView.as_view(), name="match_view"),
    path("match/project/<int:pk>", MatchProjectView.as_view(), name="match_view"),
    path("match/project/matched/<int:pk>", MatchProjectMatchedView.as_view(), name="match_view"),
    path("match/<int:pk>", MatchDetail.as_view(), name="match_detail"),
]
