from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import Payment
from api.serializers import PaymentSerializer

class PaymentListApiView(APIView):
  # method get
  def get(self, request, *args, **kwargs):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # method post
  def post(self, request, *args, **kwargs):
    data = {
      'customer': request.data.get('customer'),
      'total_payment': request.data.get('total_payment'),
      'payment_type': request.data.get('payment_type'),
    }
    serializer = PaymentSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_201_CREATED,
        'message': 'Data created successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class PaymentDetailApiView(APIView):
  # get object id
  def get_object(self, id):
    try:
      return Payment.objects.get(id=id)
    except Payment.DoesNotExist:
      return None
  
  def get(self, request, id, *args, **kwargs):
    payment_instance = self.get_object(id)
    if not payment_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    serializer = PaymentSerializer(payment_instance)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data retrieved successfully',
      'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)
  
  # method put
  def put(self, request, id, *agrs, **kwargs):
    payment_instance = self.get_object(id)
    if not payment_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    data = {
      'customer': request.data.get('customer'),
      'total_payment': request.data.get('total_payment'),
      'payment_type': request.data.get('payment_type'),
      'status': request.data.get('status'),
    }

    serializer = PaymentSerializer(instance=payment_instance, data=data, partial=True)
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