from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import Car
from api.serializers import CarSerializer

class CarListApiView(APIView):
  # method get
  def get(self, request, *args, **kwargs):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
      'category': request.data.get('category'),
      'name': request.data.get('name'),
      'price': request.data.get('price'),
      'fuel_type': request.data.get('fuel_type'),
      'baggage_capacity': request.data.get('baggage_capacity'),
      'seats': request.data.get('seats'),
      'plate_number': request.data.get('plate_number'),
      'year': request.data.get('year'),
      'location_car': request.data.get('location_car'),
      'rating' : request.data.get('rating'),
      'status_car': request.data.get('status_car'),
    }
    serializer = CarSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_201_CREATED,
        'message': 'Data created successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDetailApiView(APIView):
  # get object id
  def get_object(self, id):
    try:
      return Car.objects.get(id=id)
    except Car.DoesNotExist:
      return None
  
  def get(self, request, id, *args, **kwargs):
    table_car_instance = self.get_object(id)
    if not table_car_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    serializer = CarSerializer(table_car_instance)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data retrieved successfully',
      'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)
  
  # method put
  def put(self, request, id, *agrs, **kwargs):
    car_instance = self.get_object(id)
    if not car_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    data = {
      'category': request.data.get('category'),
      'name': request.data.get('name'),
      'price': request.data.get('price'),
      'fuel_type': request.data.get('fuel_type'),
      'baggage_capacity': request.data.get('baggage_capacity'),
      'seats': request.data.get('seats'),
      'plate_number': request.data.get('plate_number'),
      'year': request.data.get('year'),
      'location_car': request.data.get('location_car'),
      'image_car': request.data.get('image_car'),
      'rating' : request.data.get('rating'),
      'status_car': request.data.get('status_car'),
      'status': request.data.get('status')
    }

    serializer = CarSerializer(instance=car_instance, data=data, partial=True)
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