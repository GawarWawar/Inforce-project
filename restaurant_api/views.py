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
def menus (request: HttpRequest, restaurant_id = None):
    if request.method == "GET": 
        if restaurant_id:
            particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
            restaurant_menus = models.Menu.objects.filter(restaurant = particular_restaurant)
            
            particular_restaurant = serializers.RestaurantSerializer(particular_restaurant)
            restaurant_menus = serializers.MenuSerializer(restaurant_menus, many = True)
            return Response({"restaurant": particular_restaurant.data, "menus": restaurant_menus.data})
        
        all_menus = serialize_all_model_objects(
            models.Menu,
            serializers.MenuSerializer
        )
        return Response({"menus": all_menus.data})
    
    elif request.method == "POST":
        if restaurant_id:
            request.data["restaurant"] = restaurant_id
        new_menu = serializers.MenuSerializer(data = request.data)
        if new_menu.is_valid():
            new_menu.save()
            
            return Response({"menu": new_menu.data})
        else:
            return Response(new_menu.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
                
            particular_menu = get_object_or_404(models.Restaurant, pk = menu_id)
            
            changed = False
            for field in request.data:
                if particular_menu.__dict__[field] != request.data[field]:
                    particular_menu.__dict__[field] = request.data[field]
                    changed = True
            particular_menu.save()


            if restaurant_id:
                particular_restaurant = serializers.RestaurantSerializer(particular_restaurant)
                particular_menu = serializers.MenuSerializer(particular_menu)
                return Response({"restaurant": particular_restaurant.data, "menu": particular_menu.data, "changed": changed})

            return Response({"menu": particular_menu.data, "changed": changed})

@api_view(["GET"])      
def menus_filter_by_field_and_value(request, filter_field, filter_value):
    if request.method == "GET":
        menus_after_filter = models.Menu.objects.filter(**{filter_field: filter_value}) 
        menus_after_filter = serializers.MenuSerializer(menus_after_filter, many = True)
        return Response({"menus": menus_after_filter.data})
    
@api_view(["GET", "POST"])
def votes(request):
    if request.method == "GET": 
        all_votes = serialize_all_model_objects(
            models.Vote,
            serializers.VoteSerializer
        )
        return Response({"votes": all_votes.data})
    elif request.method == "POST":
        new_vote = serializers.VoteSerializer(data = request.data)
        if new_vote.is_valid():
            new_vote.save()
            
            return Response({"vote": new_vote.data})
        else:
            return Response(new_vote.errors, status=status.HTTP_400_BAD_REQUEST)