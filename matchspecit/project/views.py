from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from matchspecit.project.models import Project
from matchspecit.project.serializers import ProjectSerializer


class ProjectView(APIView):
    """
    Retrieve or post a project instance.

    * Only authenticated users are able to access this view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"serializer.data": 200, "status": status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.

    * Only authenticated users are able to access this view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk: int) -> Response:
        """
        :param pk:
        :return:
        """
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
