from django.http import HttpRequest
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from restaurant_api import models
from restaurant_api.data_manipulations import restaurants as dm_restaurants
from restaurant_api.data_manipulations import menus as dm_menus
from restaurant_api.data_manipulations import votes as dm_votes

@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(["GET", "POST"])
def restaurants(request: HttpRequest):
    if request.method == "GET": 
        return Response(dm_restaurants.get_all_restaurants())
    
    elif request.method == "POST":
        response = dm_restaurants.post_new_restaurant(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)

@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(["GET", "PUT"])      
def restaurants_by_id(request: HttpRequest, restaurant_id):
        if request.method == "GET": 
            particular_restaurant = dm_restaurants.get_restaurant_by_id(restaurant_id)
            if 'details' in particular_restaurant:
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

@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(["GET"])      
def restaurants_filter_by_field_and_value(request, filter_field, filter_value):
    if request.method == "GET":
        return Response(dm_restaurants.filter_restaurants(filter_field, filter_value))
    
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["GET", "POST"])      
def restaurants_by_id_last_menu(request: HttpRequest, restaurant_id):
        if request.method == "GET": 
            particular_restaurant = dm_restaurants.get_restaurant_by_id(restaurant_id)
            if 'details' in particular_restaurant:
                response_status = particular_restaurant.pop("status")
                return Response(particular_restaurant, status=response_status)
            else:
                particular_restaurant = particular_restaurant["restaurant"]
            
            last_restaurant_menu_id = models.Menu.objects.filter(
                restaurant = models.Restaurant.objects.get(pk = restaurant_id)
            ).last()
            
            if last_restaurant_menu_id is None:
                last_restaurant_menu_id = -1
            else:
                last_restaurant_menu_id = last_restaurant_menu_id.pk
            restaurant_menu = dm_menus.get_menu_by_id(
                last_restaurant_menu_id
            )
            if not "details" in restaurant_menu:
                restaurant_menu = restaurant_menu["menu"]
                restaurant_menu["votes"] = dm_votes.filter_votes("menu", restaurant_menu["id"])["votes"]   
            else:
                response_status = restaurant_menu.pop("status")
                return Response(restaurant_menu, status=response_status)
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