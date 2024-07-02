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
from restaurant_api import views as restaurants_views

urlpatterns = [
    path("", views.index),
    path('admin/', admin.site.urls),
    
    path("api/restaurants", restaurants_views.restaurants),
    path("api/restaurants/<restaurant_id>", restaurants_views.restaurants_by_id),
    
    path("api/restaurants/<restaurant_id>/menus", restaurants_views.menus),
    path("api/restaurants/<restaurant_id>/menus/<menu_id>", restaurants_views.menus),
    
    path("api/menus", restaurants_views.menus),
    path("api/menus/filter/<filter_field>=<filter_value>", restaurants_views.menus_filter_by_field_and_value),
    path("api/menus/<menu_id>", restaurants_views.menus_by_id),
    
    path("api/auth/", include("user_auth.urls")),
]