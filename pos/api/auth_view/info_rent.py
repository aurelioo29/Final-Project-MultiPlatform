from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from pos_app.models import InfoRent, StatusModel
from api.serializers import InfoRentSerializer

class InfoRentView(APIView):
  authentication_classes = [SessionAuthentication, BasicAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kwargs):
    cars = InfoRent.objects.select_related('status').filter(status=StatusModel.objects.first())
    serializer = InfoRentSerializer(cars, many=True)
    response = {
        'status': status.HTTP_200_OK,
        'message': 'Data retrieved successfully',
        'user': str(request.user),
        'auth': str(request.auth),
        'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)