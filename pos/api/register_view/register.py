from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import User, StatusModel
# package for handle register-user
from api.serializers import RegiserUserSerializer, LoginSerializer
from rest_framework import generics

# handle register user
class RegisterUserApiView(APIView):
  serializer_class = RegiserUserSerializer

  def post(self, request, format = None):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      serializer.save()
      response_data = {
        'status': status.HTTP_201_CREATED,
        'message': 'User created successfully',
        'data': serializer.data
      }
      return Response(response_data, status=status.HTTP_201_CREATED)
    return Response({
      'status': status.HTTP_400_BAD_REQUEST,
      'data': serializer.errors
    }, status.HTTP_400_BAD_REQUEST )
  
  def get(self, request, format = None):
    users = User.objects.all()
    serializer = RegiserUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# handle get by id user & delete user
class RegisterDetail(APIView):
  def get_object(self, id):
    try:
      return User.objects.get(id=id)
    except User.DoesNotExist:
      return None
  
  def get(self, request, id, format = None):
    user_instance = self.get_object(id)
    if not user_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    serializer = RegiserUserSerializer(user_instance)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data retrieved successfully',
      'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)
  
  def delete(self, request, id, format = None):
    user_instance = self.get_object(id)
    if not user_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    user_instance.delete()
    return Response(
      {
        'status': status.HTTP_200_OK,
        'message': 'Data deleted successfully',
        'data': {}
      }, status=status.HTTP_200_OK
    )