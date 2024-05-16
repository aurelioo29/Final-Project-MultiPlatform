from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import Customer
from api.serializers import CustomerSerializer

class CustomerListApiView(APIView):
  # method get
  def get(self, request, *args, **kwargs):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # method post
  def post(self, request, *args, **kwargs):
    data = {
      'no_ktp': request.data.get('no_ktp'),
      'name': request.data.get('name'),
      'email': request.data.get('email'),
      'phone_number': request.data.get('phone_number'),
      'location_pickup': request.data.get('location_pickup'),
      'duration': request.data.get('duration'),
      'rent_type': request.data.get('rent_type'),
      'select_car': request.data.get('select_car'),
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
      return Customer.objects.get(id=id)
    except Customer.DoesNotExist:
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
      'no_ktp': request.data.get('no_ktp'),
      'name': request.data.get('name'),
      'email': request.data.get('email'),
      'phone_number': request.data.get('phone_number'),
      'image_ktp': request.data.get('image_ktp'),
      'location_pickup': request.data.get('location_pickup'),
      'duration': request.data.get('duration'),
      'rent_type': request.data.get('rent_type'),
      'select_car': request.data.get('select_car'),
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