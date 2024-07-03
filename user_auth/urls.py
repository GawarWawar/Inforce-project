from django.urls import path, include
from . import views

urlpatterns = [
    path("signup", view=views.signup),
    path("login", view=views.login),
    path("check_token", view=views.check_token),
    path("users", view=views.users),
    path("users/<user_id>", view=views.users_by_id),
]