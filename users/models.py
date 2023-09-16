from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=50)


class City(models.Model):
    name = models.CharField(max_length=50)


class User(AbstractUser):
    country = models.ForeignKey(Country, default=None, null=True, on_delete=models.SET_DEFAULT)
    city = models.ForeignKey(City, default=None, null=True, on_delete=models.SET_DEFAULT)
    number_telephone = models.CharField(max_length=60)
    photo = models.ImageField()



