from django.urls import path

from matchspecit.match.views import MatchDetail, MatchView

urlpatterns = [
    path("match/", MatchView.as_view(), name="match_view"),
    path("match/<int:pk>", MatchDetail.as_view(), name="match_detail"),
]
