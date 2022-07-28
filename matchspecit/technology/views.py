from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchspecit.technology.models import Technology
from matchspecit.technology.serializers import TechnologySerializer

response_schema_dict = {
    "200": openapi.Response(
        description="Custom 200 response",
        examples={
            "application/json": [
                {"id": "1", "name": "Python"},
                {"id": "2", "name": "Java"},
                {"id": "3", "name": "Javascript"},
            ]
        },
    )
}


class TechnologyView(APIView):
    """
    Retrieve a technologies instances list.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        technology = Technology.objects.all()
        serializer = TechnologySerializer(technology, many=True)
        return Response(serializer.data)
