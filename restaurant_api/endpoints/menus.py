import datetime
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from restaurant_api.data_manipulations import restaurants as dm_restaurants
from restaurant_api.data_manipulations import menus as dm_menus
from restaurant_api.data_manipulations import votes as dm_votes

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