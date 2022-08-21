from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchspecit.match.models import Match
from matchspecit.match.serializers import (
    MatchPatchSerializer,
    MatchProjectSerializer,
    MatchSerializer,
    MatchSpecialistSerializer,
)

DEFAULT_SUCCESS_RESPONSE = openapi.Response(
    description="Custom 200 response",
    examples={
        "application/json": [
            {
                "id": 72,
                "user": {
                    "id": 3,
                    "username": "admin",
                    "first_name": "",
                    "last_name": "",
                    "email": "admin@example.com",
                    "is_active": True,
                    "description": None,
                    "is_matchable": True,
                    "technologies": [],
                },
                "project": {
                    "id": 3,
                    "title": "test_specjalista",
                    "description": "test",
                    "created_at": "2022-08-20T14:18:05.310291Z",
                    "updated_at": "2022-08-20T14:18:05.310309Z",
                    "owner": 2,
                    "is_matchable": True,
                    "is_finish": False,
                    "is_successful": False,
                    "is_deleted": False,
                    "technologies": [4, 5, 6],
                    "image": None,
                },
                "match_percent": "1.50",
                "project_owner_approved": None,
                "specialist_approved": None,
            },
            {
                "id": 73,
                "user": {
                    "id": 4,
                    "username": "test2",
                    "first_name": "",
                    "last_name": "",
                    "email": "",
                    "is_active": True,
                    "description": "",
                    "is_matchable": True,
                    "technologies": [1, 2, 3],
                },
                "project": {
                    "id": 3,
                    "title": "test_specjalista",
                    "description": "test",
                    "created_at": "2022-08-20T14:18:05.310291Z",
                    "updated_at": "2022-08-20T14:18:05.310309Z",
                    "owner": 2,
                    "is_matchable": True,
                    "is_finish": False,
                    "is_successful": False,
                    "is_deleted": False,
                    "technologies": [4, 5, 6],
                    "image": None,
                },
                "match_percent": "1.00",
                "project_owner_approved": None,
                "specialist_approved": None,
            },
        ]
    },
)

DEFAULT_NOT_FOUND_RESPONSE = openapi.Response(
    description="Custom 404 response", examples={"application/json": {"detail": "Not found."}}
)

DEFAULT_AUTHENTICATION_RESPONSE = openapi.Response(
    description="Custom 404 response", examples={"application/json": {"detail": "Not found."}}
)

get_match_view_response_schema_dict = {
    "200": openapi.Response(
        description="Custom 200 response",
        examples={
            "application/json": [
                {
                    "id": 72,
                    "user": {
                        "id": 3,
                        "username": "admin",
                        "first_name": "",
                        "last_name": "",
                        "email": "admin@example.com",
                        "is_active": True,
                        "description": None,
                        "is_matchable": True,
                        "technologies": [],
                    },
                    "project": {
                        "id": 3,
                        "title": "test_specjalista",
                        "description": "test",
                        "created_at": "2022-08-20T14:18:05.310291Z",
                        "updated_at": "2022-08-20T14:18:05.310309Z",
                        "owner": 2,
                        "is_matchable": True,
                        "is_finish": False,
                        "is_successful": False,
                        "is_deleted": False,
                        "technologies": [4, 5, 6],
                        "image": None,
                    },
                    "match_percent": "1.50",
                    "project_owner_approved": None,
                    "specialist_approved": None,
                },
                {
                    "id": 73,
                    "user": {
                        "id": 4,
                        "username": "test2",
                        "first_name": "",
                        "last_name": "",
                        "email": "",
                        "is_active": True,
                        "description": "",
                        "is_matchable": True,
                        "technologies": [1, 2, 3],
                    },
                    "project": {
                        "id": 3,
                        "title": "test_specjalista",
                        "description": "test",
                        "created_at": "2022-08-20T14:18:05.310291Z",
                        "updated_at": "2022-08-20T14:18:05.310309Z",
                        "owner": 2,
                        "is_matchable": True,
                        "is_finish": False,
                        "is_successful": False,
                        "is_deleted": False,
                        "technologies": [4, 5, 6],
                        "image": None,
                    },
                    "match_percent": "1.00",
                    "project_owner_approved": None,
                    "specialist_approved": None,
                },
            ]
        },
    )
}


def check_owner_or_specialist(user_id: int, match: Match):
    """
    :param user_id:
    :param match:
    :return:
    """
    if user_id == match.project.owner_id or user_id == match.user_id:
        return True
    return False


def get_object(pk: int) -> Response:
    """
    :param pk:
    :return:
    """
    try:
        return Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        raise Http404


class MatchSpecialistView(APIView):
    """
    Retrieve a matches for specialist instance list.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=get_match_view_response_schema_dict)
    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        matches = Match.objects.filter(user_id=self.request.user.id).exclude(specialist_approved__isnull=False)
        serializer = MatchSpecialistSerializer(matches, many=True)
        return Response(serializer.data)


get_match_detail_response_schema_dict = {
    "200": DEFAULT_SUCCESS_RESPONSE,
    "401": DEFAULT_AUTHENTICATION_RESPONSE,
    "404": DEFAULT_NOT_FOUND_RESPONSE,
}

patch_match_detail_request_schema_dict = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "project_owner_approved": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "specialist_approved": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)


class MatchSpecialistMatchedView(APIView):
    """
    Retrieve a matched matches for specialist instance list.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=get_match_view_response_schema_dict)
    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        matches = (
            Match.objects.filter(user_id=self.request.user.id)
            .filter(specialist_approved=True)
            .filter(project_owner_approved=True)
        )
        serializer = MatchSpecialistSerializer(matches, many=True)
        return Response(serializer.data)


class MatchProjectView(APIView):
    """
    Retrieve a matches for project instance list.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=get_match_view_response_schema_dict)
    def get(self, request: Request, pk: int) -> Response:
        """
        :param request:
        :return:
        """
        matches = Match.objects.filter(project__id=pk).exclude(project_owner_approved__isnull=False)
        serializer = MatchProjectSerializer(matches, many=True)
        return Response(serializer.data)


class MatchProjectMatchedView(APIView):
    """
    Retrieve a matched matches for project instance list.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=get_match_view_response_schema_dict)
    def get(self, request: Request, pk: int) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        matches = (
            Match.objects.filter(project__id=pk).filter(specialist_approved=True).filter(project_owner_approved=True)
        )
        serializer = MatchProjectSerializer(matches, many=True)
        return Response(serializer.data)


class MatchDetail(APIView):
    """
    Retrieve a match instance.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=get_match_detail_response_schema_dict)
    def get(self, request: Request, pk: int) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        match = get_object(pk)
        if check_owner_or_specialist(request.user.id, match):
            serializer = MatchSerializer()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(request_body=patch_match_detail_request_schema_dict)
    def patch(self, request: Request, pk: int, format=None) -> Response:
        """
        :param request:
        :param pk:
        :return:
        """
        match = get_object(pk)
        if check_owner_or_specialist(request.user.id, match):
            serializer = MatchPatchSerializer(match, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
