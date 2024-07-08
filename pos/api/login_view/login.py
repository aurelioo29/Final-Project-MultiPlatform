from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
# package for handle token
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from api.serializers import LoginSerializer
from rest_framework.permissions import AllowAny

# handle login user
class LoginView(APIView):
  permission_classes = [AllowAny]
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