from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=2)
    confirmed = models.IntegerField("confirmed", default=0)
    recovered = models.IntegerField("recovered", default=0)
    deaths = models.IntegerField("deaths", default=0)
    mortality = models.DecimalField("mortality", decimal_places=2, max_digits=5, default=0)
    last_updated = models.DateTimeField("last_updated")

    class Meta:
        indexes = [
            models.Index(fields=['name', 'code'])
        ]
    
    def __str__(self):
        return f"{self.name}"


class Date(models.Model):
    datetime = models.DateTimeField("datetime")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    confirmed = models.IntegerField("confirmed", default=0)
    recovered = models.IntegerField("recovered", default=0)
    deaths = models.IntegerField("deaths", default=0)

    class Meta:
        indexes = [
            models.Index(fields=['datetime', 'country'])
        ]

    def __str__(self):
        return f"{self.datetime} in {self.country}, " \
                f"confirmed: {self.confirmed}, " \
                f"recovered: {self.recovered}, " \
                f"deaths: {self.deaths}"
