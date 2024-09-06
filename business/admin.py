from django.contrib import admin

from .models import *
from core.models import CustomUser
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'username', 'user', 'first_name', 'last_name', 'date_joined', 'station']


class CustomerSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'sub_code', 'status', 'customer', 'customer', 'num_of_days_left', 'day_usage']

    
admin.site.register(ChargingStation)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerSubscription, CustomerSubscriptionAdmin)
admin.site.register(ChargingActivity)
admin.site.register(CustomUser)
