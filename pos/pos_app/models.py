import sys
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime, timedelta

# Custom Function 
def compress_image(image, filename):
  curr_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
  im = Image.open(image)
  if im.mode != 'RGB':
    im = im.convert('RGB')
  im_io = BytesIO()
  im.save(im_io, 'jpeg', quality = 50, optimize = True)
  im.seek(0)
  new_image = InMemoryUploadedFile(im_io, 'ImageField', '%', str(filename) + '-' + str(curr_datetime) + '.jpeg', 'image/jpeg', sys.getsizeof(im_io), None)
  return new_image

# Create your models here.
class User(AbstractUser):
  is_admin = models.BooleanField(default=False)
  is_customer = models.BooleanField(default=False)

  def __str__(self):
    return str(self.username)
# ========================================================================================================
class StatusModel(models.Model):
  choices_status = (
    ('Aktif', 'Aktif'),
    ('Tidak Aktif', 'Tidak Aktif')
  )

  name = models.CharField(max_length = 50, unique = True)
  description = models.TextField(blank=True, null=True)
  status = models.CharField(max_length = 50, choices = choices_status, default = 'Aktif')
  user_create = models.ForeignKey(User, related_name='user_create_status_model', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_status_model', blank=True, null=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.status)
# ========================================================================================================
class Profile(models.Model):
  user = models.OneToOneField(User, related_name='user_profile', on_delete=models.PROTECT)
  phone_number = models.CharField(max_length=15, default='None')
  no_ktp = models.IntegerField(unique=True, default=0)
  image_ktp = models.ImageField(default=None, upload_to='profile_images/', blank=True, null=True)
  status = models.ForeignKey(StatusModel, related_name='profile_status', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_profile', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_profile', blank=True, null=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.user} - {self.user.id}'
  
  def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
    if self.id:
      try:
        this = Profile.objects.get(id=self.id)
        if this.image_ktp != self.image_ktp:
          var_image_ktp = self.image_ktp
          self.image_ktp = compress_image(var_image_ktp, 'ktp')
          this.image_ktp.delete()
      except: pass
      super(Profile, self).save(*args, **kwargs)
    else:
      if self.image_ktp:
        var_image_ktp = self.image_ktp
        self.image_ktp = compress_image(var_image_ktp, 'ktp')
      super(Profile, self).save(*args, **kwargs)
# ========================================================================================================
class CarCategory(models.Model):
  type_choices = (
    ('Sedan', 'Sedan'),
    ('SUV', 'SUV'),
    ('LCGC', 'LCGC'),
  )

  transmission_choices = (
    ('Manual', 'Manual'),
    ('Automatic', 'Automatic')
  )

  type_car = models.CharField(max_length=50, choices=type_choices, default='None')
  type_transmission = models.CharField(max_length=50, choices=transmission_choices, default='None')
  status = models.ForeignKey(StatusModel, related_name='car_category_status', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_car_category', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_car_category', blank=True, null=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.type_car) + ' - ' + str(self.type_transmission)
# ========================================================================================================
class Car(models.Model):
  fuel_choices = (
    ('Bensin', 'Bensin'),
    ('Solar', 'Solar'),
  )
  car_choices = (
    ('Avalaible', 'Avalaible'),
    ('Not Avalaible', 'Not Avalaible'),
  )

  category = models.ForeignKey(CarCategory, related_name='car_category', on_delete=models.PROTECT)
  name_car = models.CharField(max_length=100, unique=True)
  price_day = models.DecimalField(max_digits=10, decimal_places=2)
  fuel_type = models.CharField(max_length=50, choices=fuel_choices, default='Bensin')
  baggage_capacity = models.IntegerField()
  seats = models.IntegerField()
  plate_number = models.CharField(max_length=50, unique=True)
  year = models.PositiveIntegerField()
  location_car = models.CharField(max_length=100)
  image_car = models.ImageField(default = None, upload_to='car_images/', blank=True, null=True)
  rating = models.FloatField(default=0.0, blank=True, null=True)
  status_car = models.CharField(max_length=50, choices=car_choices, default='Avalaible')
  status = models.ForeignKey(StatusModel, related_name='car_model_status', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_car', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_car', blank=True, null=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.name) + ' with price ' + str(self.price)
  
  def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
    if self.id:
      try:
        this = Car.objects.get(id=self.id)
        if this.image_car != self.image_car:
          var_image_car = self.image_car
          self.image_car = compress_image(var_image_car, 'car')
          this.image_car.delete()
      except: pass
      super(Car, self).save(*args, **kwargs)
    else:
      if self.image_car:
        var_image_car = self.image_car
        self.image_car = compress_image(var_image_car, 'car')
      super(Car, self).save(*args, **kwargs)
# ========================================================================================================
def generate_code_book():
  last_code = Booking.objects.all().order_by('code').last()
  if not last_code:
    return 'BOK00001'
  code = last_code.code
  code_number = int(code[3:7])
  new_code = code_number + 1
  return 'BOK' + str(new_code).zfill(5)
class Booking(models.Model):
  rent_choices = (
    ('With Driver', 'With Driver'),
    ('Without Driver', 'Without Driver')
  )

  # no_ktp = models.IntegerField(unique=True)
  # name = models.CharField(max_length=100)
  # email = models.EmailField(max_length=100, unique=True)
  # phone_number = models.CharField(max_length=15)
  # image_ktp = models.ImageField(default=None, upload_to='customer_images/', blank=True, null=True)
  select_car = models.ForeignKey(Car, related_name='car_booking', on_delete=models.PROTECT, default=1)
  name_booking = models.ForeignKey(User, related_name='user_booking', on_delete=models.PROTECT)
  code_book = models.CharField(max_length=20, editable=False, default=generate_code_book)
  date_rental = models.DateTimeField()
  date_return = models.DateTimeField()
  location_pickup = models.CharField(max_length=100)
  quantity = models.IntegerField()
  rent_type = models.CharField(max_length=50, choices=rent_choices, default='With Driver')
  status = models.ForeignKey(StatusModel, related_name='customer_status', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_customer', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_customer', blank=True, null=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.name)
# ========================================================================================================
class Payment(models.Model):
  payment_choices = (
    ('Cash', 'Cash'),
  )

  customer = models.ForeignKey(Booking, related_name='customer_payment', on_delete=models.PROTECT)
  total_payment = models.DecimalField(max_digits=10, decimal_places=2)
  payment_type = models.CharField(max_length=50, choices=payment_choices, default='None')
  status = models.ForeignKey(StatusModel, related_name='payment_status', default=StatusModel.objects.first().pk, on_delete=models.PROTECT)
  user_create = models.ForeignKey(User, related_name='user_create_payment', blank=True, null=True, on_delete=models.SET_NULL)
  user_update = models.ForeignKey(User, related_name='user_update_payment', blank=True, null=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.customer) + ' - ' + str(self.total_payment)
# ========================================================================================================