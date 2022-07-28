from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchspecit.technology.models import Technology
from matchspecit.user.permissions import IsActive, OwnProfilePermission
from matchspecit.user.serializers import UserSerializer


get_response_schema_dict = {
    "200": openapi.Response(
        description="Custom 200 response",
        examples={"application/json": {"technologies": [{"id": "1", "name": "python"}], "is_matchable": True}},
    )
}

patch_response_schema_dict = {
    "200": openapi.Response(
        description="Custom 200 response",
        examples={"application/json": {"technologies": [{"id": "1", "name": "python"}], "is_matchable": True}},
    )
}

delete_response_schema_dict = {
    "204": openapi.Response(description="Custom 204 response", examples={"application/json": ""})
}

patch_request_schema_dict = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "is_matchable": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "technologies": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_STRING, description="identifier"),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, description="technology name"),
                },
            ),
        ),
    },
)


class UserView(APIView):
    """
    Retrieve or update a user.

    * Only authenticated and owner user is able to access this view.
    """

    permission_classes = (OwnProfilePermission, permissions.IsAuthenticated, IsActive)

    @swagger_auto_schema(responses=get_response_schema_dict)
    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(responses=patch_response_schema_dict, request_body=patch_request_schema_dict)
    def patch(self, request: Request, *args, **kwargs) -> Response:
        """
        :param request:
        :return:
        """
        data = {}

        if technology_ids := request.data.get("technology_ids"):
            technologies = Technology.objects.filter(id__in=technology_ids).values("id", "name")
            data.update({"technologies": list(technologies)})

        if "is_matchable" in request.data:
            data.update({"is_matchable": request.data.get("is_matchable")})

        serializer = UserSerializer(
            instance=request.user,
            data=data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses=delete_response_schema_dict)
    def delete(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
