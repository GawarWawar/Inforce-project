from rest_framework import status

from restaurant_api import serializers, models
from . import tools

def get_all_restaurants():
    """
        Vrapper of function serialize_filtered_model_objects with specified model and serializer
    """
    all_restaurants = tools.serialize_filtered_model_objects(
        {"all": True},
        models.Restaurant,
        serializers.RestaurantSerializer
    )
    return {"restaurants": all_restaurants.data}
    
def post_new_restaurant(request_data):
    """
        Validate restaurant through Serializer and return it or details
    """
    new_restaurant = serializers.RestaurantSerializer(data = request_data)
    if new_restaurant.is_valid():
        new_restaurant.save()
        
        return {"restaurant": new_restaurant.data}
    else:
        return {"details": new_restaurant.errors, "status": status.HTTP_400_BAD_REQUEST}
    
def get_restaurant_by_id(restaurant_id):
    """
        Vrapper of function get_object_by_id with specified object_name_string, model and serializer
    """
    return tools.get_object_by_id(restaurant_id, "restaurant", models.Restaurant, serializers.RestaurantSerializer)
    
def update_restaurant_by_id(request_data, restaurant_id):
    """
        Vrapper of function update_object with specified object_name_string, model and serializer
    """
    return tools.update_object(
        request_data, restaurant_id, "restaurant", models.Restaurant, serializers.RestaurantSerializer
    )
    
def filter_restaurants(filter_field, filter_value):
    """
    Vrapper of function serialize_filtered_model_objects with specified object_name_string, model and serializer
    """
    filtered_data = tools.serialize_filtered_model_objects(
        {filter_field: filter_value},
        models.Restaurant,
        serializers.RestaurantSerializer
    ).data
    return {"restaurant": filtered_data}