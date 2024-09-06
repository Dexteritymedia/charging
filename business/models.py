import uuid
import base64
import datetime
import string
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe

# Create your models here.
User = get_user_model()

def generate_verification_code():
    uuid_code = uuid.uuid1()
    sub_code = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=25))
    return sub_code


class ChargingStation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    slug = models.SlugField(default=uuid.uuid4, editable=False, null=True)
    address = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='stations', null=True, blank=True)
    
    def __str__(self):
        return self.name.title()

    def station_picture(self):
        if self.picture:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" /.>' %(self.picture)
                )
        return None
    
class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, blank=True, unique=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now, null=True, blank=True)
    station = models.ForeignKey(ChargingStation, null=True, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return f'User {self.pk}'

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return None

class CustomerSubscription(models.Model):
    STATUS  = (
        (0, 'Not charging'),
        (1, 'Charging'),
        (2, 'Charged'),
    )
    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name="customer")
    sub_date = models.DateTimeField(default=timezone.now, null=True)
    expiry_date = models.DateTimeField(blank=True)
    sub_code = models.CharField(max_length=300, default=generate_verification_code, unique=True, blank=True, null=True)
    status = models.CharField(max_length=10, default=STATUS[1], choices=STATUS, blank=True, null=True)
    usage = models.PositiveIntegerField(blank=True, default=0)
    day_usage = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f'User {self.pk}'
        #return self.customer.user.username

    def get_full_name(self):
        if self.customer__first_name and self.customer__last_name:
            return f'{self.customer__first_name} {self.customer__last_name}'
        return None

    def num_of_days_left(self):
        expiry_date = datetime.datetime.strptime(str(self.expiry_date.date()), '%Y-%m-%d')
        today = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        days_left = expiry_date - today
        if expiry_date < today:
            return 'Expired'
        else:
            return days_left.days

    def save(self, *args, **kwargs):
        print('Date', self.sub_date)
        self.expiry_date =  self.sub_date.date() + datetime.timedelta(days=30)
        print(self.expiry_date)
        
        return super(CustomerSubscription, self).save(*args, **kwargs)

    

class ChargingActivity(models.Model):
    sub_code = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    device = models.CharField(max_length=30, blank=True, null=True)
    subscriber = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='activity')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Charging Activities'

    def __str__(self):
        return f'Charging Activity by {self.subscriber} on {self.date}'
