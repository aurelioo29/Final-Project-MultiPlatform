from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import User, StatusModel
from api.serializers import RegiserUserSerializer
# modules main view
from api.main_view.payment import PaymentListApiView, PaymentDetailApiView
from api.main_view.customer import CustomerListApiView, CustomerDetailApiView
from api.main_view.car_category import CarCategoryListApiView, CarCategoryDetailApiView
from api.main_view.car import CarListApiView, CarDetailApiView
# modules auth view
from api.auth_view.car import CarView
from api.auth_view.car_category import CarCategoryView
from api.auth_view.customer import CustomerView
from api.auth_view.payment import PaymentView
# modules filter car
from api.filter_view.filter import CarFilterApi
# modules register user
from api.register_view.register import RegisterUserApiView
from api.register_view.register import RegisterDetail
# modules login user
from api.login_view.login import LoginView

