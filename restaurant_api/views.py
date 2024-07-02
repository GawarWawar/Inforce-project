import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest

from . import models, serializers
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
            
@api_view(["GET"])      
def restaurants_filter_by_field_and_value(request, filter_field, filter_value):
    if request.method == "GET":
        return Response(dm_restaurants.filter_restaurants(filter_field, filter_value))
    
@api_view(["GET", "POST"])      
def restaurants_by_id_last_menu(request: HttpRequest, restaurant_id):
        if request.method == "GET": 
            particular_restaurant = dm_restaurants.get_restaurant_by_id(restaurant_id)
            if 'errors' in particular_restaurant:
                response_status = particular_restaurant.pop("status")
                return Response(particular_restaurant, status=response_status)
            else:
                particular_restaurant = particular_restaurant["restaurant"]
            
            restaurant_menu = serializers.MenuSerializer(
                models.Menu.objects.filter(
                    restaurant = models.Restaurant.objects.get(pk = restaurant_id)
                ).last()
            ).data
            
            
            restaurant_menu["votes"] = dm_votes.filter_votes("menu", restaurant_menu["id"])["votes"]   
            return Response(
                {
                    "restaurant": particular_restaurant, 
                    "menu": restaurant_menu
                }
            )
        
        if request.method == "POST":
            response = dm_restaurants.get_restaurant_by_id(restaurant_id)
            if "error" in response:
                response_status = response.pop("status")
                return Response(response, status=response_status)

            request.data["restaurant"] = restaurant_id
            response = dm_menus.post_new_menu(request.data)
            if "error" in response:
                response_status = response.pop("status")
                return Response(response, status=response_status)
            else:
                return Response(response)


@api_view(["GET", "POST"])
def all_menus (request: HttpRequest):
    if request.method == "GET": 
        return Response(dm_menus.get_all_menus())
    
    elif request.method == "POST":            
        response = dm_menus.post_new_menu(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)
        
@api_view(["GET"])
def menus_current_day (request: HttpRequest):
    if request.method == "GET": 
        return Response(dm_menus.filter_menus("day_created", datetime.date.today()))
        
        
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
        response = dm_votes.post_vote(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)
        
@api_view(["GET", "PUT"])
def votes_by_id(request, vote_id):
    if request.method == "GET": 
        particular_vote = dm_votes.get_vote_by_id(vote_id)
        if 'errors' in particular_vote:
            response_status = particular_vote.pop("status")
            return Response(particular_vote, status=response_status)
        else:
            return Response(particular_vote.pop("vote"))
        
    if request.method == "PUT":
        response = dm_votes.update_vote_by_id(request.data, vote_id)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)
        
@api_view(["GET"])      
def votes_filter_by_field_and_value(request, filter_field, filter_value):
    if request.method == "GET":
        return Response(dm_votes.filter_votes(filter_field, filter_value))