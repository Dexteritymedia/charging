import string
import random
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import *

def generate_subscription_code():
    sub_code = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=25))
    return sub_code


def generate_referral_code():
    ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return ref_code

def daily_charging_activity(request, station, sub_code, device=None, subscriber=None):
    customer = get_object_or_404(CustomerSubscription, customer__station__name=station, sub_code=sub_code)
    print(customer.num_of_days_left())
    today = datetime.datetime.now(timezone.utc)
    
    activity = ChargingActivity()

    
    activity = ChargingActivity.objects.filter(
        Q(subscriber__user__username=customer.customer.user)|Q(subscriber__username=customer.customer.username)
    ).last()
    
    print("Act", activity)
    if today <= customer.expiry_date:
        if today.date() != activity.date and customer.day_usage < 2:
            customer.day_usage += 1
            customer.status = 1
            customer.save()

            activity.date = today
            activity.sub_code = sub_code
            
            if device != None:
                activity.device = device
    
            if subscriber != None:
                activity.name = subscriber
                activity.subscriber = customer.customer
            else:
                activity.subscriber = customer.customer
                
            activity.time = datetime.datetime.now(timezone.utc).time()
            activity.save()
            print('completed')
            messages.info(request, 'Your device is charging!')
    
        else:
            print("You have exhausted today's subscription. Please come back tomorrow")
            messages.error(request, "You have exhausted today's subscription. Please come back tomorrow")
    else:
        print('Your subscription has expired! Please subscribe')
        messages.error(request, 'Your subscription has expired! Please subscribe')

    
    #try:
    #except CustomerSubscription.DoesNotExist:


#update daily usage: CustomerSubscription.objects.all().update(day_usage=0)
#update daily usage: CustomerSubscription.objects.filter(expiry_date__gte=datetime.datetime.now(timezone.utc)).update(day_usage=0)
