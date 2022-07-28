from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchspecit.project.models import Project
from matchspecit.project.serializers import ProjectSerializer

DEFAULT_SUCCESS_RESPONSE = openapi.Response(
    description="Custom 200 response", examples={"application/json": {"name": "test name"}}
)

DEFAULT_NOT_FOUND_RESPONSE = openapi.Response(
    description="Custom 404 response", examples={"application/json": {"detail": "Not found."}}
)

DEFAULT_AUTHENTICATION_RESPONSE = openapi.Response(
    description="Custom 404 response", examples={"application/json": {"detail": "Not found."}}
)


get_project_view_response_schema_dict = {
    "200": openapi.Response(description="Custom 200 response", examples={"application/json": [{"name": "test name"}]})
}

post_project_view_response_schema_dict = {
    "200": openapi.Response(
        description="Custom 200 response", examples={"application/json": {"serializer.data": 200, "status": 201}}
    )
}


class ProjectView(APIView):
    """
    Retrieve or post a project instance.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=get_project_view_response_schema_dict)
    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses=post_project_view_response_schema_dict)
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


get_project_detail_response_schema_dict = {
    "200": DEFAULT_SUCCESS_RESPONSE,
    "401": DEFAULT_AUTHENTICATION_RESPONSE,
    "404": DEFAULT_NOT_FOUND_RESPONSE,
}

put_project_detail_response_schema_dict = {
    "200": DEFAULT_SUCCESS_RESPONSE,
    "401": DEFAULT_AUTHENTICATION_RESPONSE,
    "404": DEFAULT_NOT_FOUND_RESPONSE,
}

put_project_detail_request_schema_dict = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

delete_project_detail_response_schema_dict = {
    "204": openapi.Response(description="Custom 204 response", examples={"application/json": ""}),
    "401": DEFAULT_AUTHENTICATION_RESPONSE,
    "404": DEFAULT_NOT_FOUND_RESPONSE,
}


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

    @swagger_auto_schema(responses=get_project_detail_response_schema_dict)
    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses=put_project_detail_response_schema_dict, request_body=put_project_detail_request_schema_dict
    )
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

    @swagger_auto_schema(responses=delete_project_detail_response_schema_dict)
    def delete(self, request: Request, pk: int, format=None) -> Response:
        
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
