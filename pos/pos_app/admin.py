from django.contrib import admin
# from pos_app.models import User, StatusModel, Profile, CarCategory, Car, Customer, Payment, InfoRent
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.StatusModel)
admin.site.register(models.Profile)
admin.site.register(models.CarCategory)
admin.site.register(models.Car)
admin.site.register(models.Customer)
admin.site.register(models.Payment)
admin.site.register(models.InfoRent)