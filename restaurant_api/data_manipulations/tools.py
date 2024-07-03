from restaurant_api import serializers, models
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status


def serialize_filtered_model_objects(
    filter: dict,
    model: models.models.Model,
    serializer: serializers.serializers.Serializer
) -> serializers.serializers.Serializer:
    """
        Filter models objects by the filter, serialize them by Serializer
    """
    if "all" in filter:
        return serializer(model.objects.all(), many = True)
    else:
        return serializer(model.objects.filter(**filter), many = True)

def update_object(
        data_to_update, object_id, object_name_string, object_model, object_serializer
) -> dict[str, str]|dict[str, dict]:
    """
        Check if object exists and then update it
    """
    try: 
        object_to_change = get_object_or_404(object_model, pk = object_id)
    except Http404 as error:
        return {"details": error, "status": status.HTTP_404_NOT_FOUND}
    
    changed = False
    for field in data_to_update:
        try:
            if object_to_change.__dict__[field] != data_to_update[field]:
                object_to_change.__dict__[field] = data_to_update[field]
                changed = True
        except KeyError as error:
            return {"details": "Bad key "+str(error), "status": status.HTTP_400_BAD_REQUEST}
            
    try:
        object_to_change.save()
    except IntegrityError as error:
        return {"details": str(error), "status": status.HTTP_300_MULTIPLE_CHOICES}
        
    object_to_change = object_serializer(
        object_model.objects.get(pk = object_id)
    )
    return {object_name_string: object_to_change.data, "changed": changed}

def get_object_by_id (object_id, object_name_string, model, serializer) -> dict[str, str]|dict[str, dict]:  
    """
        Check if object exists and return all information about it
    """         
    try:
        particular_object = get_object_or_404(model, pk = object_id)
    except Http404 as error:
        return {"details": str(error), "status": status.HTTP_404_NOT_FOUND}
    particular_object = serializer(particular_object)
    return {object_name_string: particular_object.data}