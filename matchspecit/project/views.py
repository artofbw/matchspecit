from django.http import Http404, HttpResponseForbidden
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchspecit.project.models import Project
from matchspecit.project.serializers import ProjectSerializer

DEFAULT_SUCCESS_RESPONSE = openapi.Response(
    description="Custom 200 response",
    examples={
        "application/json": {
            "id": 39,
            "title": "test",
            "description": "test",
            "created_at": "2022-07-30T15:59:38.491271Z",
            "updated_at": "2022-07-30T15:59:38.491289Z",
            "owner": 2,
            "is_matchable": True,
            "is_finish": False,
            "is_successful": False,
            "is_deleted": False,
            "technologies": [6],
            "image": "/files/covers/image.png",
        }
    },
)

DEFAULT_NOT_FOUND_RESPONSE = openapi.Response(
    description="Custom 404 response", examples={"application/json": {"detail": "Not found."}}
)

DEFAULT_AUTHENTICATION_RESPONSE = openapi.Response(
    description="Custom 404 response", examples={"application/json": {"detail": "Not found."}}
)

get_project_view_response_schema_dict = {
    "200": openapi.Response(
        description="Custom 200 response",
        examples={
            "application/json": [
                {
                    "id": 39,
                    "title": "test",
                    "description": "test",
                    "created_at": "2022-07-30T13:44:43.177660Z",
                    "updated_at": "2022-07-30T14:12:36.485120Z",
                    "owner": 1,
                    "is_matchable": True,
                    "is_finish": False,
                    "is_successful": False,
                    "is_deleted": False,
                    "technologies": [3, 4, 5],
                    "image": "/files/covers/image.png",
                },
                {
                    "id": 40,
                    "title": "test2",
                    "description": "test2",
                    "created_at": "2022-07-30T14:16:13.249097Z",
                    "updated_at": "2022-07-30T14:16:13.249117Z",
                    "owner": 1,
                    "is_matchable": True,
                    "is_finish": False,
                    "is_successful": False,
                    "is_deleted": False,
                    "technologies": [74, 75, 76],
                    "image": "/files/covers/image_1.png",
                },
            ]
        },
    )
}

post_project_view_response_schema_dict = {
    "200": openapi.Response(
        description="Custom 200 response", examples={"application/json": {"serializer.data": 200, "status": 201}}
    )
}

post_project_view_request_schema_dict = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["title", "description", "technologies"],
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "is_matchable": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "is_finish": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "is_successful": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "is_deleted": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "technologies": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
        ),
        "image": openapi.Schema(type=openapi.TYPE_STRING),
    },
)


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

    @swagger_auto_schema(
        responses=post_project_view_response_schema_dict, request_body=post_project_view_request_schema_dict
    )
    def post(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        serializer = ProjectSerializer(data=request.data, context={"request": request})
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

    def check_owner(self, pk: int, request: Request):
        if request.user.id != Project.objects.get(pk=pk).owner_id:
            print(request.user.id)
            print(Project.objects.get(pk=pk).owner_id)
            return False
        return True

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
        if self.check_owner(pk, request):
            serializer = ProjectSerializer(project, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(responses=delete_project_detail_response_schema_dict)
    def delete(self, request: Request, pk: int, format=None) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        if self.check_owner(pk, request):
            project = self.get_object(pk)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
