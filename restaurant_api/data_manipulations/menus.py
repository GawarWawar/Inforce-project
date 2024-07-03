from rest_framework import status

from restaurant_api import serializers, models
from . import tools

def get_all_menus():
    all_menus = tools.serialize_filtered_model_objects(
        {"all": True},
        models.Menu,
        serializers.MenuSerializer
    )
    return {"menus": all_menus.data}

def post_new_menu(request_data):
    new_menu = serializers.MenuSerializer(data = request_data)
    if new_menu.is_valid():
        new_menu.save()
        
        return {"menu": new_menu.data}
    else:
        return {"details": new_menu.details, "status": status.HTTP_400_BAD_REQUEST}

def get_menu_by_id(menu_id):
    return tools.get_object_by_id(menu_id, "menu", models.Menu, serializers.MenuSerializer)
    
def update_menu_by_id(request_data, menu_id):
    return tools.update_object(
        request_data, menu_id, "menu", models.Menu, serializers.MenuSerializer
    )

def filter_menus(filter_field, filter_value):
    filtered_data = tools.serialize_filtered_model_objects(
        {filter_field: filter_value},
        models.Menu,
        serializers.MenuSerializer
    ).data
    return {"menus": filtered_data}