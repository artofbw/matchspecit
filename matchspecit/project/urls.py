from django.urls import path

from matchspecit.project.views import ProjectView, ProjectDetail

urlpatterns = [
    path('project/', ProjectView.as_view(), name="project_view"),
    path('project/<int:pk>', ProjectDetail.as_view(), name="project_detail"),
]
