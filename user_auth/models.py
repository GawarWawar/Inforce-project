from django.db import models
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Create your models here.
class Employee(User):
    
    user_permissions = [
        ("can_vote", "Can vote")
    ]
    
class RestourantEmployee(User):
    user_permissions = [
       ("add_menu", "Can add menu")
    ]

class Admin (User):
    ...