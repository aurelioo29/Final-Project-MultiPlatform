from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import Booking
from api.serializers import CustomerSerializer

class CustomerListApiView(APIView):
  # method get
  def get(self, request, *args, **kwargs):
    customers = Booking.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # method post
  def post(self, request, *args, **kwargs):
    data = {
      'select_car': request.data.get('select_car'),
      'name_booking': request.data.get('name_booking'),
      'date_rental': request.data.get('date_rental'),
      'date_return': request.data.get('date_return'),
      'location_pickup': request.data.get('location_pickup'),
      'quantity': request.data.get('quantity'),
      'rent_type': request.data.get('rent_type'),
    }
    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_201_CREATED,
        'message': 'Data created successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class CustomerDetailApiView(APIView):
  # get object id
  def get_object(self, id):
    try:
      return Booking.objects.get(id=id)
    except Booking.DoesNotExist:
      return None
  
  def get(self, request, id, *args, **kwargs):
    customer_instance = self.get_object(id)
    if not customer_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    serializer = CustomerSerializer(customer_instance)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data retrieved successfully',
      'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)
  
  # method put
  def put(self, request, id, *agrs, **kwargs):
    customer_instance = self.get_object(id)
    if not customer_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    data = {
      'select_car': request.data.get('select_car'),
      'name_booking': request.data.get('name_booking'),
      'date_rental': request.data.get('date_rental'),
      'date_return': request.data.get('date_return'),
      'location_pickup': request.data.get('location_pickup'),
      'quantity': request.data.get('quantity'),
      'rent_type': request.data.get('rent_type'),
      'status': request.data.get('status')
    }

    serializer = CustomerSerializer(instance=customer_instance, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_200_OK,
        'message': 'Data updated successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # method delete
  def delete(self, request, id, *args, **kwargs):
    car_category_instance = self.get_object(id)
    if not car_category_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    car_category_instance.delete()
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data deleted successfully',
    }
    return Response(response, status=status.HTTP_200_OK)