from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest


from . import serializers, models

def serialize_all_model_objects(
    model: models.models.Model,
    serializer: serializers.serializers.Serializer
) -> serializers.serializers.Serializer:
    return serializer(model.objects.all(), many = True)
    

@api_view(["GET", "POST"])
def restaurants(request: HttpRequest):
    if request.method == "GET": 
        all_restaurants = serialize_all_model_objects(
            models.Restaurant,
            serializers.RestaurantSerializer
        )
        return Response({"restaurants": all_restaurants.data})
    
    elif request.method == "POST":
        new_resourant = serializers.RestaurantSerializer(data = request.data)
        if new_resourant.is_valid():
            new_resourant.save()
            restaurant = models.Restaurant.objects.get(name = request.data["name"])
            
            return Response({"restaurant": new_resourant.data})
        else:
            return Response(new_resourant.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(["GET", "PUT"])      
def restaurants_by_id(request: HttpRequest, restaurant_id):
        if request.method == "GET": 
            particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
            restaurant_menus = models.Menu.objects.filter(restaurant = particular_restaurant)
            
            particular_restaurant = serializers.RestaurantSerializer(particular_restaurant)
            restaurant_menus = serializers.MenuSerializer(restaurant_menus, many = True)
            return Response({"restaurant": particular_restaurant.data, "menus": restaurant_menus.data})
        
        if request.method == "PUT":
            particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
            
            changed = False
            for field in request.data:
                if particular_restaurant.__dict__[field] != request.data[field]:
                    particular_restaurant.__dict__[field] = request.data[field]
                    changed = True
            particular_restaurant.save()

            particular_restaurant = serializers.RestaurantSerializer(
                models.Restaurant.objects.get(pk = restaurant_id)
            )

            return Response({"restaurant": particular_restaurant.data, "changed": changed})

@api_view(["GET", "POST"])
def menus (request: HttpRequest):
    if request.method == "GET": 
        all_menus = serialize_all_model_objects(
            models.Menu,
            serializers.MenuSerializer
        )
        return Response({"menu": all_menus.data})
    
    elif request.method == "POST":
        new_menu = serializers.RestaurantSerializer(data = request.data)
        if new_menu.is_valid():
            new_menu.save()
            
            return Response({"menu": new_menu.data})
        else:
            return Response(new_menu.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET", "PUT"])      
def menus_by_id(request: HttpRequest, menu_id):
        if request.method == "GET": 
            particular_menu = models.Menu.objects.filter(pk = menu_id)
            
            particular_menu = serializers.MenuSerializer(particular_menu, many = True)
            return Response({"menu": particular_menu.data})
        
        if request.method == "PUT":
            particular_menu = get_object_or_404(models.Restaurant, pk = menu_id)
            
            changed = False
            for field in request.data:
                if particular_menu.__dict__[field] != request.data[field]:
                    particular_menu.__dict__[field] = request.data[field]
                    changed = True
            particular_menu.save()

            particular_menu = serializers.RestaurantSerializer(
                models.Restaurant.objects.get(pk = menu_id)
            )

            return Response({"menu": particular_menu.data, "changed": changed})
