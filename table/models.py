from django.conf import settings
from django.db import models
from django.utils import timezone


class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    gangs = models.IntegerField(blank=True, default = 0)
    forts = models.IntegerField(blank=True, default = 0)
    fights = models.IntegerField(blank=True, default = 0)
    zvz = models.IntegerField(blank=True, default = 0)
    accepted_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.nickname