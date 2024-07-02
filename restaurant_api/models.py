from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from user_auth.models import Employee

import datetime
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField("Name",unique=True, max_length=200)
    description = models.CharField("Description", max_length=1000, default=None)
    stars = models.IntegerField("Stars", default=0)
    
class Menu(models.Model):
    restaurant  = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_created = models.DateField("Day of creation", default=datetime.date.today)
    description = models.CharField("Description", max_length=1000, default=0)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, verbose_name="Menu of the day", on_delete=models.CASCADE)
    day_of_vote = models.DateField("Day of vote", default=datetime.date.today)
    
    class Meta:
        unique_together = ['user', 'menu', "day_of_vote"]