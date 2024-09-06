import os
import datetime
from datetime import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.db.models import Q

import pandas as pd

from .forms import CustomerChargingForm, CustomerSubscriptionForm, CustomerSignUpForm
from .models import *
from .utils import *
from .tasks import scrape_club_history
# Create your views here.


def home(request):
    return render(request, 'business/Tail-home.html') #home, F-home, Tail-home

def scrape_data(request):
    data =[]
    for season in seasons:
            results = scrape_club_history(season)
            print(results)
            print("Compiling...")
            data.append(results)
            print("Waiting 5 seconds to start scraping again...")
            time.sleep(5)
    print("Saving to csv")
    print(data)
    data_to_list = [i for j in data for i in j]
    df_club_history = pd.DataFrame(data_to_list)
    stor = os.path.join(root, f"static/data/brazil-teams/Cruzeiro-{season}.csv")
    print(stor)
    df_club_history.to_csv(stor)

def update_daily_usage():
    today = datetime.datetime.now(timezone.utc)
    #hour = datetime.datetime.now(timezone.utc).hour()
    #minute = datetime.datetime.now(timezone.utc).minute()
    print(today.strftime("%H:%M"))
    #eight_pm = datetime.datetime(2014, 5, 12, 23, 30)
    eight_pm = datetime.time(23, 30)
    print(eight_pm.strftime("%H:%M"))
    print(type(str(eight_pm)))
    if today == eight_pm:
        return CustomerSubscription.objects.filter(expiry_date__gte=datetime.datetime.now(timezone.utc)).update(day_usage=0)
    else:
        pass

def index(request):
    charging_stations = ChargingStation.objects.filter(status=True).all()
    context = {'stations':charging_stations}
    update_daily_usage()
    return render(request, 'business/index.html', context)


def register_customer(request, slug, name):
    
    charging_station = ChargingStation.objects.get(slug=slug, name=name)
    print(charging_station)
    form = CustomerSignUpForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            print(username)
            print(first_name)
            print(last_name)

            all_users = Customer.objects.all()

            for user in all_users:
                if str(username) in str(user.user):
                    messages.error(request, f"Username '{username}' already exists")
                    return render(request, 'business/register-customer.html', {'form':form})

            customer = Customer.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                station=charging_station,
            )

            customer_sub = CustomerSubscription.objects.create(
                customer=customer,
            )
            #customer_sub = customer.customer
            print(customer_sub)
            return redirect('station-customer', charging_station.name, charging_station.slug)
        else:
           print(f"{form.errors}")
           messages.error(request, f"{form.errors}")
    else:
        form = CustomerSignUpForm()
    context = {'form':form} 
    return render(request, 'business/register-customer.html', context)


def station_customer(request, slug, name):
    charging_station = ChargingStation.objects.get(slug=slug, name=name)
    #ChargingStation.objects.filter(customer__customer=name)
    #print(charging_station_customer_set__customer.all())
    customers = Customer.objects.filter(station=charging_station)
    print(customers)
    customer_codes = []
    expiry_dates = []
    status = []
    num_of_days_left = []
    for customer_code in customers:

        #customer = customer_code.customer.all().values_list('customer__username', 'customer__user__username').distinct()
        customer = customer_code.customer.all().values_list('customer__username', flat=True).distinct()
        if customer[0] == None:
            print('======')
            customer = customer_code.customer.all().values_list('customer__user__username', flat=True).distinct()
        #customer = customer_code.customer.all().values_list(Q('customer__username', flat=True)|Q('customer__user__username', flat=True)).distinct()
        print('Customer', str(customer))
        
        result = CustomerSubscription.objects.filter(Q(customer__user__username=customer[0])|Q(customer__username=customer[0])).last()
        print(result.status)
        customer_codes.append(result.sub_code)
        expiry_dates.append(result.expiry_date)
        status.append(result.status)
        num_of_days_left.append(result.num_of_days_left)
        for item in customer:
            print(item)
            #customer_codes.append(item.sub_code)
            #expiry_dates.append(item.expiry_date)
            #status.append(item.status)
            
    
    context = {
        'station': charging_station,
        'customers': customers,
        'customer_items': zip(customers, customer_codes, expiry_dates, status, num_of_days_left),
    }
    return render(request, 'business/station-customer.html', context)


def customer_subscription(request, slug, name, customer_username, user_id):
    charging_station = ChargingStation.objects.get(slug=slug, name=name, status=True)
    print(charging_station)
    customer = Customer.objects.get(Q(user__username=customer_username, id=user_id)|Q(username=customer_username, id=user_id))
    #customer = Customer.objects.get(user__username=customer_username)
    print("ID", customer.id)
    #customer_sub = CustomerSubscription.objects.filter(customer__user__username=customer).last()
    customer_sub = CustomerSubscription.objects.filter(Q(customer__user__username=customer)|Q(customer__username=customer_username)).last()
    
    if customer_sub.customer.user == None:
        user = customer_sub.customer.username
        print("USername", user)
    else:
        user = customer_sub.customer.user.username
        print("USer", user)
        
    if customer_sub is None:
        customer_sub = CustomerSubscription.objects.create(
                customer=customer,
                sub_date=timezone.now(),
            )
        print(f"Your subscription has been activated! It will expire on {customer_sub.expiry_date}")
        
        url = reverse('subscribed', args=[user])
        url_with_params = f"{url}?subscription+customer={user}&sub_date={customer_sub.sub_date}&expiry_date={customer_sub.expiry_date}&"
        return HttpResponseRedirect(url_with_params)
    else:
        #print(customer_sub.expiry_date)

        print(datetime.datetime.now(timezone.utc))
        if customer_sub.expiry_date < datetime.datetime.now(timezone.utc):
            customer_sub = CustomerSubscription.objects.create(
                customer=customer,
                sub_date=timezone.now(),
            )
            print(f"Your subscription has been activated! It will expire on {customer_sub.expiry_date}")
            #return redirect('subscribed', customer_sub.customer.username)
            url = reverse('subscribed', args=[user])
            url_with_params = f"{url}?subscription+customer={user}&sub_date={customer_sub.sub_date}&expiry_date={customer_sub.expiry_date}&"
            return HttpResponseRedirect(url_with_params)
        else:
            print(f"Your subscription hasn't expired! It will expire on {customer_sub.expiry_date}")
            messages.error(request, f"Your subscription hasn't expired! It will expiry on {customer_sub.expiry_date}")
            #return redirect('index')
            return redirect('subscribed', user)
    context = {}
    return render(request, 'business/customer-subscription.html', context)


def subscription_activated(request, name):
    customer_sub = CustomerSubscription.objects.filter(
        Q(customer__user__username=name)|Q(customer__username=name)
    ).filter(
            #expiry_date__gte=datetime.datetime.now(timezone.utc)
            ).order_by('-sub_date').all()
    print(customer_sub)
    context = {'customer_sub': customer_sub}
    return render(request, 'business/subscription.html', context)


def customer_details(request, id, customer_username=None):
    #customer = get_object_or_404(Customer, user__username=customer_username)
    try:
        customer = Customer.objects.get(Q(user__username=customer_username, id=id)|Q(username=customer_username, id=id))
    except Customer.DoesNotExist:
        raise Http404
    activities = ChargingActivity.objects.filter(subscriber=customer).order_by('-date')
    context = {'customer':customer, 'activities':activities}
    return render(request, 'business/customer-details.html', context)


def customer_charging_act(request, slug, name, code=None):
    charging_station = get_object_or_404(ChargingStation, slug=slug, name=name, status=True)
    print('Slug', charging_station.slug)
    if code is not None:
        print(code)
        daily_charging_activity(request, station=charging_station.name, sub_code=code)
        return redirect('station-customer', charging_station.name, charging_station.slug)
    else:
        form = CustomerChargingForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                sub_code = form.cleaned_data['sub_code']
                customer_name = form.cleaned_data['name']
                device = form.cleaned_data['device']

                customer = CustomerSubscription.objects.get(sub_code=sub_code)
                print(type(customer.status))
                if customer.status == str(1):
                    print("Charging Act", customer.status)
                    messages.error(request, 'There is a device currently charging')
                else:
                    daily_charging_activity(request, station=charging_station.name, sub_code=sub_code, device=device, subscriber=customer_name)
        return render(request, 'business/search_sub_code.html', {'form':form})

def stop_charging(request, customer_name, code):
   
    try:
        customer = CustomerSubscription.objects.get(Q(customer__user__username=customer_name, sub_code=code)|Q(customer__username=customer_name, sub_code=code))
    except CustomerSubscription.DoesNotExist:
        pass
    print(customer.customer.station.name)
    customer.status = 2
    customer.save()
    return redirect('station-customer', customer.customer.station.name, customer.customer.station.slug)
