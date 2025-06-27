from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ApartmentType(models.Model):
    name = models.CharField(max_length=30)  # type

    def __str__(self):
        return self.name


class AnimalsAllowed(models.Model):
    status = models.CharField(max_length=30)  # type

    def __str__(self):
        return self.status


class RentalApartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)  # adresse
    type = models.ForeignKey(ApartmentType, on_delete=models.CASCADE)
    size = models.IntegerField()  # størrelse
    rooms = models.IntegerField()  # antal værelser
    monthlyRent = models.IntegerField()  # månedlig husleje
    securityDeposit = models.CharField(max_length=30)  # depositum
    prepaidRent = models.IntegerField()  # forudbetalt leje
    animalsAllowed = models.ForeignKey(AnimalsAllowed, on_delete=models.CASCADE)  # husdyr (se om det skal være boolean)

    balcony = models.BooleanField(blank=True, default=False)  # altan
    garden = models.BooleanField(blank=True, default=False)  # garden
    elevator = models.BooleanField(blank=True, default=False)  # elevator
    furnished = models.BooleanField(blank=True, default=False)  # møbleret
    parking = models.BooleanField(blank=True, default=False)  # parkering

    title = models.CharField(max_length=255)  # titel
    description = models.TextField()  # beskrivelse

    email = models.EmailField()  # email
    phoneNumber = models.CharField(max_length=31, blank=True)  # telefonnummer

    ##

    rentalPeriod = models.DateField(auto_now_add=True)  # lejeperiode
    availableFrom = models.DateTimeField(null=True)  # ledig fra

    floor = models.IntegerField()  # etage
    energyLabel = models.CharField(max_length=30)  # energimærke

    timestamp = models.DateTimeField(auto_now_add=True)  # timestamp

    def __str__(self):
        return self.title


class ApartmentImage(models.Model):
    rental_apartment = models.ForeignKey(RentalApartment, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images/')

    def __str__(self):
        return str(self.rental_apartment.title)


class SavedApartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rentalApartment = models.ForeignKey(RentalApartment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.rentalApartment.title

    class Meta:
        unique_together = ('rentalApartment', 'user')

#https://ilovedjango.com/django/admin/login-with-email-instead-of-user-name-in-django-admin/

class ReportRentalApartment(models.Model):
    rentalApartment = models.ForeignKey(RentalApartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rentalApartment', 'user')

    def __str__(self):
        return self.title

class FollowApartment(models.Model):
    rentalApartment = models.ForeignKey(RentalApartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rentalApartment', 'user')