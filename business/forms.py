from django import forms

from .models import CustomerSubscription, Customer

class CustomerChargingForm(forms.Form):
    sub_code = forms.CharField()
    name = forms.CharField(help_text='Customer name',)
    device = forms.CharField(help_text='Name of charging device. For example, phone',)


class CustomerSubscriptionForm(forms.Form):
    customer = forms.CharField()

class CustomerSignUpForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username','first_name','last_name',]
