from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    
    path('', views.index, name='index'),
    path('station/<name>/<slug>/', views.station_customer, name='station-customer'),
    path('<name>/subscribed/', views.subscription_activated, name='subscribed'),
    path('<name>/<slug>/charge/', views.customer_charging_act, name='charging-act'),
    path('<name>/<slug>/charge/<code>/', views.customer_charging_act, name='charging-act'),
    path('<slug>/<name>/customer-registration/', views.register_customer, name='register-customer'),
    path('<id>/<customer_username>/', views.customer_details, name='customer-details'),
    path('stop-charging/<code>/<customer_name>/', views.stop_charging, name='stop-charging'),
    path('<name>/<slug>/subscribe/<customer_username>/<user_id>/', views.customer_subscription, name='customer-subscription'),
]
