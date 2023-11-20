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

class Feedback(models.Model):
    given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class League(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Trophy(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)

class TeamType(models.Model):
    type = models.CharField(max_length=255)

class Team(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(TeamType, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Player(models.Model):
    name = models.CharField(max_length=255)
    jersey_number = models.IntegerField(max_length=2)
    country = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    club = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True) 
    trophies = models.ManyToManyField(Trophy, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)
    scheduled_date_and_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)