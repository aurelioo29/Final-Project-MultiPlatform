from rest_framework import serializers
from pos_app.models import User, StatusModel, Profile, CarCategory, Car, Booking, Payment
from django.contrib.auth import authenticate # import authenticate for register feature
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# static view
class RegiserUserSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
  password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_active', 'is_admin']
    extra_kwargs = {
      'username': {'required': True},
    }
  
  def validate(self, attrs):
    if attrs['password1'] != attrs['password2']:
      raise serializers.ValidationError({
        'password': 'Password 1 and Password 2 does not same'
      })
    return attrs
  
  def create(self, validated_data):
    user = User.objects.create(
      first_name = validated_data['first_name'],
      last_name = validated_data['last_name'],
      username = validated_data['username'],
      email = validated_data['email'],
      is_active = validated_data['is_active'],
      is_admin = validated_data['is_admin']
    )
    user.set_password(validated_data['password1'])
    user.is_staff = validated_data.get('is_admin', False)
    user.save()
    return user

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    username = data.get('username', '')
    password = data.get('password', '')

    if username and password:
      user = authenticate(username=username, password=password)
      if user:
        if user.is_active and user.is_admin:
          data['user'] = user
        else:
          msg = 'Status user is not active or not admin'
          raise ValidationError({'message' : msg})
      else:
        msg = "You don't have permission to access this page"
        raise ValidationError({'message' : msg})
    else:
      msg = 'Must fill colomn username and password'
      raise ValidationError({'message' : msg})
    return data

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('id', 'user', 'phone_number', 'no_ktp', 'image_ktp', 'status')


# main view
class CarCategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = CarCategory
    fields = ('id', 'type_car', 'type_transmission', 'status')

class CarSerializer(serializers.ModelSerializer):
  class Meta:
    model = Car
    fields = ('id', 'category', 'name_car', 'price_day',
              'fuel_type', 'baggage_capacity', 'seats',
              'plate_number', 'year', 'location_car',
              'image_car', 'rating', 'status_car', 'status'
              )

class CustomerSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Booking
    fields = ('id', 'select_car', 'name_booking', 
              'code_book', 'date_rental', 'date_return',
              'location_pickup', 'quantity', 'rent_type', 
              'status'
              )

class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = ('id', 'customer', 'total_payment', 'payment_type', 'status')