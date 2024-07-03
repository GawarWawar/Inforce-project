from restaurant_api import serializers, models
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status


def serialize_filtered_model_objects(
    filter: dict,
    model: models.models.Model,
    serializer: serializers.serializers.Serializer
) -> serializers.serializers.Serializer:
    if "all" in filter:
        return serializer(model.objects.all(), many = True)
    else:
        return serializer(model.objects.filter(**filter), many = True)

def update_object(data_to_update, object_id, object_name_string, object_model, object_serializer):
    try: 
        object_to_change = get_object_or_404(object_model, pk = object_id)
    except Http404 as error:
        return {"details": error, "status": status.HTTP_404_NOT_FOUND}
    
    changed = False
    for field in data_to_update:
        if object_to_change.__dict__[field] != data_to_update[field]:
            object_to_change.__dict__[field] = data_to_update[field]
            changed = True
            
    object_to_change.save()
    object_to_change = object_serializer(
        object_model.objects.get(pk = object_id)
    )
    return {object_name_string: object_to_change.data, "changed": changed}

def get_object_by_id (object_id, object_name_string, model, serializer):           
    try:
        particular_object = get_object_or_404(model, pk = object_id)
    except Http404 as error:
        return {"details": str(error), "status": status.HTTP_404_NOT_FOUND}
    particular_object = serializer(particular_object)
    return {object_name_string: particular_object.data}