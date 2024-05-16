from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import User, StatusModel
# package for handle register-user
from api.serializers import RegiserUserSerializer, LoginSerializer
from rest_framework import generics
# package for handle token
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
# modules main view
from api.main_view.info_rent import InfoRentListApiView, InfoRentDetailApiView
from api.main_view.payment import PaymentListApiView, PaymentDetailApiView
from api.main_view.customer import CustomerListApiView, CustomerDetailApiView
from api.main_view.car_category import CarCategoryListApiView, CarCategoryDetailApiView
from api.main_view.car import CarListApiView, CarDetailApiView
# modules auth view
from api.auth_view.car import CarView
from api.auth_view.car_category import CarCategoryView
from api.auth_view.customer import CustomerView
from api.auth_view.info_rent import InfoRentView
from api.auth_view.payment import PaymentView
# modules pagination
from .paginators import CustomPagination
from api.serializers import CarSerializer
from pos_app.models import Car
# package for filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# handle filter car
class CarFilterApi(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category__type_car', 'category__type_transmission', 'name']
    ordering_fields = ['created_on']

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

# handle login user
class LoginView(APIView):
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    django_login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return JsonResponse({
      'status': status.HTTP_200_OK,
      'message': 'Login successfully',
      'data': {
        'token': token.key,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_admin': user.is_admin,
      }
    })