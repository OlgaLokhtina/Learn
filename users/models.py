from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'



class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class User(AbstractUser):
    country = models.ForeignKey(Country, default=None, null=True, on_delete=models.SET_DEFAULT)
    city = models.ForeignKey(City, default=None, null=True, on_delete=models.SET_DEFAULT)
    number_telephone = models.CharField(max_length=60)
    photo = models.ImageField(upload_to="users")


