from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest


from . import serializers, models
from .data_manipulations import restaurants as dm_restaurants
from .data_manipulations import menus as dm_menus
from .data_manipulations import votes as dm_votes
    

@api_view(["GET", "POST"])
def restaurants(request: HttpRequest):
    if request.method == "GET": 
        return Response(dm_restaurants.get_all_restaurants(request))
    
    elif request.method == "POST":
        response = dm_restaurants.post_new_restaurant(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)
  
@api_view(["GET", "PUT"])      
def restaurants_by_id(request: HttpRequest, restaurant_id):
        if request.method == "GET": 
            # particular_restaurant = dm_restaurants.get_restaurant_by_id(restaurant_id)
            # if particular_restaurant['errors']:
            #     response_status = particular_restaurant.pop("status")
            #     return Response(particular_restaurant, status=response_status)
            # TODO: add menu by id here and votes by id for every menu
            
            
            
            particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
            restaurant_menus = models.Menu.objects.filter(restaurant = particular_restaurant)
            
            particular_restaurant = serializers.RestaurantSerializer(particular_restaurant)
            restaurant_menus = serializers.MenuSerializer(restaurant_menus, many = True)
            return Response({"restaurant": particular_restaurant.data, "menus": restaurant_menus.data})
        
        if request.method == "PUT":
            response = dm_restaurants.update_restaurant_by_id(request.data, restaurant_id)
            if "error" in response:
                response_status = response.pop("status")
                return Response(response, status=response_status)
            else:
                return Response(response)

@api_view(["GET", "POST"])
def all_menus (request: HttpRequest, restaurant_id = None):
    if request.method == "GET": 
        if restaurant_id:
            particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
            restaurant_menus = models.Menu.objects.filter(restaurant = particular_restaurant)
            
            particular_restaurant = serializers.RestaurantSerializer(particular_restaurant)
            restaurant_menus = serializers.MenuSerializer(restaurant_menus, many = True)
            return Response({"restaurant": particular_restaurant.data, "menus": restaurant_menus.data})
        
        return Response(dm_menus.get_all_menus())
    
    elif request.method == "POST":
        if restaurant_id:
            request.data["restaurant"] = restaurant_id
            
        response = dm_restaurants.post_new_restaurant(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)
        
        
@api_view(["GET", "PUT"])      
def menus_by_id(request: HttpRequest, menu_id, restaurant_id = None):
        if request.method == "GET": 
            if restaurant_id:
                tmp = menu_id
                menu_id = restaurant_id
                restaurant_id = tmp

            particular_menu = get_object_or_404(models.Menu, pk = menu_id)
            particular_menu = serializers.MenuSerializer(particular_menu)

            if restaurant_id:
                particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
                
                particular_restaurant = serializers.RestaurantSerializer(particular_restaurant)
                return Response({"restaurant": particular_restaurant.data, "menu": particular_menu.data})
        
            return Response({"menu": particular_menu.data})
            
        if request.method == "PUT":
            if restaurant_id:
                tmp = menu_id
                menu_id = restaurant_id
                restaurant_id = tmp
                particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
                
            if request.method == "PUT":
                response = dm_menus.update_menu_by_id(request.data, menu_id)
            if "error" in response:
                response_status = response.pop("status")
                return Response(response, status=response_status)
            else:
                return Response(response)

@api_view(["GET"])      
def menus_filter_by_field_and_value(request, filter_field, filter_value):
    if request.method == "GET":
        return Response(dm_menus.filter_menus(filter_field, filter_value))
    
@api_view(["GET", "POST"])
def votes(request):
    if request.method == "GET": 
        return Response(dm_votes.get_all_votes())
    elif request.method == "POST":
        new_vote = serializers.VoteSerializer(data = request.data)
        if new_vote.is_valid():
            new_vote.save()
            
            return Response({"vote": new_vote.data})
        else:
            return Response(new_vote.errors, status=status.HTTP_400_BAD_REQUEST)