from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchspecit.match.models import Match
from matchspecit.match.serializers import MatchSerializer
from matchspecit.project.models import Project

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
            "match_percent": 1.0,
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
                    "match_percent": 1.0,
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
                    "match_percent": 1.0,
                },
            ]
        },
    )
}


class MatchView(APIView):
    """
    Retrieve a matched project instance list.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=get_project_view_response_schema_dict)
    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        matches = Match.objects.filter(user_id=self.request.user.id)
        projects = [match.project for match in matches]
        serializer = MatchSerializer(projects, many=True)
        return Response(serializer.data)


get_project_detail_response_schema_dict = {
    "200": DEFAULT_SUCCESS_RESPONSE,
    "401": DEFAULT_AUTHENTICATION_RESPONSE,
    "404": DEFAULT_NOT_FOUND_RESPONSE,
}


class MatchDetail(APIView):
    """
    Retrieve a matched project instance.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def has_permission(self, user_id: int, match: Match):
        """
        :param user_id:
        :param match:
        :return:
        """
        if user_id != match.user.id:
            return False
        return True

    def get_object(self, pk: int) -> Response:
        """
        :param pk:
        :return:
        """
        try:
            return Match.objects.get(project__id=pk, user_id=self.request.user.id)
        except Project.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses=get_project_detail_response_schema_dict)
    def get(self, request: Request, pk: int) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        match = self.get_object(pk)
        if self.has_permission(self.request.user.id, match):
            serializer = MatchSerializer(match.project)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
