from django.db import models

# Create your models here.
class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    provider = models.CharField(max_length=30)
    accuracy = models.FloatField(null=True)
    altitude = models.FloatField(null=True)
    bearing = models.FloatField(null=True)
    speed = models.FloatField(null=True)
    time = models.CharField(max_length=30)
    timestamp = models.BigIntegerField(db_index=True)
    owner = models.CharField(max_length=30,db_index=True)

class KnownLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255)


