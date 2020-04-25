from django.db import models

class Province(models.Model):
    province = models.CharField(max_length=50)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"province: {self.province}, country: {self.country}"



class Country(models.Model):
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2) 
    confirmed = models.IntegerField("confirmed")
    confirmed_history = {}
    recovered = models.IntegerField("recovered")
    recovered_history = {}
    deaths = models.IntegerField("deaths")
    deaths_history = {}

    def __str__(self):
        return f"country: {self.country}," \
                f"country_code: {self.country_code}," \
                f"confirmed: {self.confirmed}," \
                f"confirmed_history: {self.confirmed_history}," \
                f"recovered: {self.recovered}," \
                f" recovered_history: {self.recovered_history}," \
                f"deaths: {self.deaths}," \
                f"deaths_history: {self.deaths_history}"
