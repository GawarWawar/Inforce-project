from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest, Http404

from restaurant_api import serializers, models
from . import tools

def get_all_restaurants():
        all_restaurants = tools.serialize_filtered_model_objects(
            {"all": True},
            models.Restaurant,
            serializers.RestaurantSerializer
        )
        return {"restaurants": all_restaurants.data}
    
def post_new_restaurant(request_data):
    new_resourant = serializers.RestaurantSerializer(data = request_data)
    if new_resourant.is_valid():
        new_resourant.save()
        
        return {"restaurant": new_resourant.data}
    else:
        return {"errors": new_resourant.errors, "status": status.HTTP_400_BAD_REQUEST}
    
def get_restaurant_by_id(restaurant_id):
    return tools.get_object_by_id(restaurant_id, models.Restaurant, serializers.RestaurantSerializer)
    
def update_restaurant_by_id(request_data, restaurant_id):
    response = tools.update_object(request_data, restaurant_id, models.Restaurant, serializers.RestaurantSerializer)
    if "error" in response:
        return response
    else:
        response["restaurant"] = response.pop("object")
        return response