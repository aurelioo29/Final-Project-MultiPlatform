from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import InfoRent
from api.serializers import InfoRentSerializer

# handle request get and post
class InfoRentListApiView(APIView):
  # method get
  def get(self, request, *args, **kwargs):
    info_rent = InfoRent.objects.all()
    serializer = InfoRentSerializer(info_rent, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # method post
  def post(self, request, *args, **kwargs):
    data = {
      # 'code': request.data.get('code'),
      # 'car': request.data.get('car'),
      'customer': request.data.get('customer'),
      'payment': request.data.get('payment'),
      'date_rent': request.data.get('date_rent'),
      'date_return': request.data.get('date_return'),
      # 'status': request.data.get('status')
    }
    serializer = InfoRentSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_201_CREATED,
        'message': 'Data created successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# handle request get, put, and delete
class InfoRentDetailApiView(APIView):
  # get object id
  def get_object(self, id):
    try:
      return InfoRent.objects.get(id=id)
    except InfoRent.DoesNotExist:
      return None
  
  def get(self, request, id, *args, **kwargs):
    rent_instance = self.get_object(id)
    if not rent_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    serializer = InfoRentSerializer(rent_instance)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data retrieved successfully',
      'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)
  
  # method put
  def put(self, request, id, *agrs, **kwargs):
    rent_instance = self.get_object(id)
    if not rent_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    data = {
      # 'code': request.data.get('code'),
      # 'car': request.data.get('car'),
      'customer': request.data.get('customer'),
      'payment': request.data.get('payment'),
      'date_rent': request.data.get('date_rent'),
      'date_return': request.data.get('date_return'),
      'status': request.data.get('status')
    }

    serializer = InfoRentSerializer(instance=rent_instance, data=data, partial=True)
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
    rent_instance = self.get_object(id)
    if not rent_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    rent_instance.delete()
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data deleted successfully',
    }
    return Response(response, status=status.HTTP_200_OK)