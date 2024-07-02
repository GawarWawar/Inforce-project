from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest, Http404

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
        return {"errors": new_menu.errors, "status": status.HTTP_400_BAD_REQUEST}

def get_menu_by_id(menu_id):
        try:
            particular_menu = get_object_or_404(models.Menu, pk = menu_id)
        except Http404 as error:
            return {"errors": error, "status": status.HTTP_404_NOT_FOUND}
        particular_menu = serializers.MenuSerializer(particular_menu)
        return {"menu": particular_menu.data}
    
def update_menu_by_id(request_data, menu_id):
    response = tools.update_object(request_data, menu_id, models.Menu, serializers.MenuSerializer)
    if "error" in response:
        return response
    else:
        response["menu"] = response.pop("object")
        return response

def filter_menus(filter_field, filter_value):
    filtered_data = tools.serialize_filtered_model_objects(
        {filter_field: filter_value},
        models.Menu,
        serializers.MenuSerializer
    ).data
    return {"menus": filtered_data}