from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"name: {self.name}, " \
                f"code: {self.code}"


class Province(models.Model):
    name = models.CharField(max_length=50, default='nan', unique=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=20, decimal_places=18, validators=[MinValueValidator(-90), MaxValueValidator(90)], unique=True)
    longitude = models.DecimalField(max_digits=21, decimal_places=19, validators=[MinValueValidator(-180), MaxValueValidator(180)], unique=True)
    confirmed = models.IntegerField("confirmed", default=0)
    confirmed_history = {}
    recovered = models.IntegerField("recovered", default=0)
    recovered_history = {}
    deaths = models.IntegerField("deaths", default=0)
    deaths_history = {}
    datetime = models.TimeField("datetime", default=datetime.now())

    def __str__(self):
        return f"name: {self.name}, " \
                f"country: {self.country}, " \
                f"latitude: {self.latitude}, " \
                f"longitude: {self.longitude}, " \
                f"confirmed: {self.confirmed}, " \
                f"confirmed_history: {self.confirmed_history}, " \
                f"recovered: {self.recovered}, " \
                f" recovered_history: {self.recovered_history}, " \
                f"deaths: {self.deaths}, " \
                f"deaths_history: {self.deaths_history}, " \
                f"datetime: {self.datetime}"

    class Meta:
        ordering = ['name']
