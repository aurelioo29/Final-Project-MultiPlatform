from django.contrib import admin
from pos_app.models import User, StatusModel
from pos_app.models import User, StatusModel, Profile, CarCategory, Car, Customer, Payment, InfoRent
# Register your models here.
admin.site.register(User)
admin.site.register(StatusModel)
admin.site.register(Profile)
admin.site.register(CarCategory)
admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(InfoRent)