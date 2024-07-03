from django.urls import path, include
from . import views

urlpatterns = [
    # Register user providing username, password and email
    path("signup", view=views.signup),
    # Login to system using username and password
    path("login", view=views.login),
    # Check if token working, returns user
    path("check_token", view=views.check_token),
    # GET all users or POST to create user
    path("users", view=views.users),
    # GET all info about certain user or PUT to edit certain user
    path("users/<user_id>", view=views.users_by_id),
]