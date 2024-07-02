from django.db import models
from django.utils import timezone

from user_auth.models import Employee

import datetime
# Create your models here.

class Restourant(models.Model):
    name = models.CharField("Name",unique=True, max_length=200)
    description = models.CharField("Description", max_length=1000, default=None)
    stars = models.IntegerField("Stars", default=0)
    
class Menu(models.Model):
    restourant  = models.ForeignKey(Restourant, on_delete=models.CASCADE)
    day_created = models.DateField("Day of creation", default=timezone.now)
    description = models.CharField("Description", max_length=1000, default=0)

class Vote(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, verbose_name="Menu of the day", on_delete=models.CASCADE)
    day_of_vote = models.DateField("Day of vote", default=timezone.now)