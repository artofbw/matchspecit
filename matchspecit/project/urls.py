from django.urls import path

from matchspecit.project.views import ProjectDetail, ProjectView

urlpatterns = [
    path('project/', ProjectView.as_view(), name="project_view"),
    path('project/<int:pk>', ProjectDetail.as_view(), name="project_detail"),
]
