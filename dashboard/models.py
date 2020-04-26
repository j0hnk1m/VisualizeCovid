from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"id: {self.id}, " \
                f"name: {self.name}, " \
                f"code: {self.code}"


class Province(models.Model):
    name = models.CharField(max_length=50, default='nan', unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    datetime = models.DateTimeField("datetime")

    def __str__(self):
        return f"name: {self.name}, " \
                f"country: {self.country}, " \
                f"datetime: {self.datetime}"

    class Meta:
        ordering = ['name']


class Coordinate(models.Model):
    latitude = models.DecimalField(max_digits=6, decimal_places=4, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=21, decimal_places=4, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    province = models.OneToOneField(Province, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"latitude: {self.latitude}, " \
                f"longitude: {self.longitude}, " \
                f"province: {self.province}"


class Stat(models.Model):
    confirmed = models.IntegerField("confirmed", default=0)
    recovered = models.IntegerField("recovered", default=0)
    deaths = models.IntegerField("deaths", default=0)
    province = models.OneToOneField(Province, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"confirmed: {self.confirmed}, " \
                f"recovered: {self.recovered}, " \
                f"deaths: {self.deaths}, " \
                f"province: {self.province}"


class Case(models.Model):
    date = models.DateField("date")
    value = models.IntegerField("value")
    CHOICES = [(c.upper(), c) for c in (['confirmed', 'recovered', 'deaths'])]
    category = models.CharField(max_length=10, choices=CHOICES)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return f"date: {self.date}, " \
                f"value: {self.value}, " \
                f"category: {self.category}, " \
                f"province: {self.province}"
