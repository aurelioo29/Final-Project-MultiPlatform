from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import CarCategory
from api.serializers import CarCategorySerializer

class CarCategoryListApiView(APIView):
  # method get
  def get(self, request, *args, **kwargs):
    car_categorys = CarCategory.objects.all()
    serializer = CarCategorySerializer(car_categorys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # method post
  def post(self, request, *args, **kwargs):
    data = {
      'type_car': request.data.get('type_car'),
      'type_transmission': request.data.get('type_transmission'),
    }
    serializer = CarCategorySerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_201_CREATED,
        'message': 'Data created successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class CarCategoryDetailApiView(APIView):
  # get object id
  def get_object(self, id):
    try:
      return CarCategory.objects.get(id=id)
    except CarCategory.DoesNotExist:
      return None
  
  def get(self, request, id, *args, **kwargs):
    table_category_instance = self.get_object(id)
    if not table_category_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    serializer = CarCategorySerializer(table_category_instance)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data retrieved successfully',
      'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)
  
  # method put
  def put(self, request, id, *agrs, **kwargs):
    car_category_instance = self.get_object(id)
    if not car_category_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    data = {
      'type_car': request.data.get('type_car'),
      'type_transmission': request.data.get('type_transmission'),
      'status': request.data.get('status')
    }

    serializer = CarCategorySerializer(instance=car_category_instance, data=data, partial=True)
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