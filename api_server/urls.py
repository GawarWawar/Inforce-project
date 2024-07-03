"""
URL configuration for api_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views
from restaurant_api.endpoints import restaurants as restaurants_views
from restaurant_api.endpoints import menus as menus_views
from restaurant_api.endpoints import votes as votes_views

urlpatterns = [
    path("", views.index),
    path('admin/', admin.site.urls),
    
    
    # MAIN ENDPOINTS
    # User authification
    path("api/auth/", include("user_auth.urls")),
    # GET all restaurants or POST to create new restaurant
    path("api/restaurants", restaurants_views.restaurants),
    # GET last menu for the particular restaurant or POST to create new menu for the restaurant
    path("api/restaurants/<restaurant_id>/menu", restaurants_views.restaurants_by_id_last_menu),
    # GET menus for the current day
    path("api/today_menus", menus_views.menus_current_day), 
    # GET all votes or POST to create new vote
    path("api/votes", votes_views.votes),
    # GET votes for each of the day`s menu
    path("api/votes/calculate_today", votes_views.votes_calculate_for_today),
    
    # ADDITIONAL ENDPOINTS
    # GET restaurant by id or PUT to update it
    path("api/restaurants/<restaurant_id>", restaurants_views.restaurants_by_id),
    # GET all restaurant where filter_field=filter_value
    path(
        "api/restaurants/filter/<filter_field>=<filter_value>", 
        restaurants_views.restaurants_filter_by_field_and_value
    ),
    # GET all menus or POST to create new menu
    path("api/menus", menus_views.all_menus),
    # GET menu by id or PUT to update it
    path("api/menus/<menu_id>", menus_views.menus_by_id),
    # GET all menus where filter_field=filter_value
    path("api/menus/filter/<filter_field>=<filter_value>", menus_views.menus_filter_by_field_and_value),
    # GET vote by id or PUT to update it
    path("api/votes/<vote_id>", votes_views.votes_by_id),
    # GET all votes where filter_field=filter_value
    path("api/votes/filter/<filter_field>=<filter_value>", votes_views.votes_filter_by_field_and_value),
]