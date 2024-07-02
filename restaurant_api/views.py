from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from . import serializers, models

@api_view(["GET", "POST"])
def restaurants(request):
    if request.method == "GET": 
        all_restaurants = models.Restaurant.objects.all()
        all_restaurants = serializers.RestaurantSerializer(all_restaurants, many = True)
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
def restaurants_by_id(request, restaurant_id):
        if request.method == "GET": 
            particular_restaurant = get_object_or_404(models.Restaurant, pk = restaurant_id)
            particular_restaurant = serializers.RestaurantSerializer(particular_restaurant)
            return Response({"restaurant": particular_restaurant.data})
        
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

