from django.contrib import admin
from .models import CarMake, CarModel, Dealer

# Register your models here.
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Dealer)
