from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'
urlpatterns = [
  path('api/car-category', views.CarCategoryListApiView.as_view()),
  path('api/car-category/<int:id>', views.CarCategoryDetailApiView.as_view()),

  path('api/car', views.CarListApiView.as_view()),
  path('api/car/<int:id>', views.CarDetailApiView.as_view()),

  path('api/customer', views.CustomerListApiView.as_view()),
  path('api/customer/<int:id>', views.CustomerDetailApiView.as_view()),

  path('api/payment', views.PaymentListApiView.as_view()),
  path('api/payment/<int:id>', views.PaymentDetailApiView.as_view()),

  path('api/register', views.RegisterUserApiView.as_view()),
  path('api/register/<int:id>', views.RegisterDetail.as_view()),

  path('api/login', views.LoginView.as_view()),

  path('api/car-view', views.CarView.as_view()),
  path('api/category-car-view', views.CarCategoryView.as_view()),
  path('api/customer-view', views.CustomerView.as_view()),
  path('api/payment-view', views.PaymentView.as_view()),

  path('api/car-filter/', views.CarFilterApi.as_view()),
]