from rest_framework import status

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
    return tools.get_object_by_id(restaurant_id, "restaurant", models.Restaurant, serializers.RestaurantSerializer)
    
def update_restaurant_by_id(request_data, restaurant_id):
    return tools.update_object(
        request_data, restaurant_id, "restaurant", models.Restaurant, serializers.RestaurantSerializer
    )
    
def filter_restaurants(filter_field, filter_value):
    filtered_data = tools.serialize_filtered_model_objects(
        {filter_field: filter_value},
        models.Restaurant,
        serializers.RestaurantSerializer
    ).data
    return {"restaurant": filtered_data}