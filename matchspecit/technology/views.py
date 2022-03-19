from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchspecit.technology.models import Technology
from matchspecit.technology.serializers import TechnologySerializer


class TechnologyView(APIView):
    """
    Retrieve a technologies instances list.

    * Only authenticated users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        :param request:
        :return:
        """
        technology = Technology.objects.all()
        serializer = TechnologySerializer(technology, many=True)
        return Response(serializer.data)
