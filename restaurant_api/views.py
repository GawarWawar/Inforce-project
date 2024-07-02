from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest, HttpResponseNotAllowed


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
            particular_restaurant = dm_restaurants.get_restaurant_by_id(restaurant_id)
            if 'errors' in particular_restaurant:
                response_status = particular_restaurant.pop("status")
                return Response(particular_restaurant, status=response_status)
            else:
                particular_restaurant = particular_restaurant["restaurant"]
            restaurant_menus = dm_menus.filter_menus("restaurant", restaurant_id)["menus"]
            
            for menu in restaurant_menus:
                menu["votes"] = dm_votes.filter_votes("menu", menu["id"])["votes"]   
            
            return Response(
                {
                    "restaurant": particular_restaurant, 
                    "menus": restaurant_menus
                }
            )
        
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
        return Response(dm_menus.get_all_menus())
    
    elif request.method == "POST":            
        response = dm_menus.post_new_menu(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)
        
        
@api_view(["GET", "PUT"])      
def menus_by_id(request: HttpRequest, menu_id):
        if request.method == "GET": 
            particular_menu = dm_menus.get_menu_by_id(menu_id)
            if 'errors' in particular_menu:
                response_status = particular_menu.pop("status")
                return Response(particular_menu, status=response_status)
            else:
                particular_menu = particular_menu.pop("menu")
            
            menu_votes = dm_votes.filter_votes("menu", particular_menu["id"])["votes"]   
            
            return Response(
                {
                    "menu": particular_menu,
                    "votes": menu_votes
                }
            )
            
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