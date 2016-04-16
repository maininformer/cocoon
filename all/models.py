from __future__ import unicode_literals

from django.db import models
from django.utils import timezone as tz

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=50)
    signup_date = models.DateTimeField(default=tz.now)

    def __unicode__(self):
        return self.name


class SoundData(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=tz.now)
    intensity = models.FloatField()
    lat = models.FloatField()
    long = models.FloatField()



