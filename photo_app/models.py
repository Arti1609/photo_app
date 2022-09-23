
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.


class PhotoShootType(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    photo = models.ImageField()


class Package(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    duration = models.IntegerField()
    sessions = models.ForeignKey(PhotoShootType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reservations(models.Model):
    date = models.DateTimeField()
    report_date = models.DateTimeField(auto_now_add=True)# data wysłania rezerwacji
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    comment = models.TextField()
    status = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)


class Image(models.Model):
    path = models.ImageField
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)
    choice = models.BooleanField(default=False) #wybór uzytkownika
