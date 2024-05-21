# modules pagination
from api.paginators import CustomPagination
from api.serializers import CarSerializer
from pos_app.models import Car
from rest_framework import generics
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class CarFilterApi(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category__type_car', 'category__type_transmission', 'name']
    ordering_fields = ['created_on']