from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):

    is_station = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username}"
