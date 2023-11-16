from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField 

# Create your models here.
class Address(models.Model):
    description = models.CharField(max_length=255)
    suite_or_pobox = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)

class UserProfile(models.Model):
    associated_user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    addresses = models.ManyToManyField(Address)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)