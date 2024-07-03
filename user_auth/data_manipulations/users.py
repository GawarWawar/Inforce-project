from rest_framework import status

from user_auth import serializers
from restaurant_api.data_manipulations import tools
from django.contrib.auth.models import User

from user_auth import tokens


def get_all_users():
        all_users = tools.serialize_filtered_model_objects(
            {"all": True},
            User,
            serializers.UserSerializer
        )
        return {"users": all_users.data}

def post_user(request_data):
    new_user = serializers.UserSerializer(data = request_data)
    if new_user.is_valid():
        new_user.save()
        user = User.objects.get(username=request_data["username"])
        user.set_password(request_data["password"])
        user.save()
        
        generated_tokens = tokens.create_jwt_pair_for_user(user)
        data = new_user.data
        data.pop("password")
        
        return {"tokens": generated_tokens, "user": data}
    else:
        return {"details": new_user.errors, "status": status.HTTP_400_BAD_REQUEST}
    
def get_user_by_id(user_id):
    return tools.get_object_by_id(user_id, "user", User, serializers.UserSerializer)    

def update_user_by_id(request_data, user_id):
    return tools.update_object(
        request_data, user_id, "user", User, serializers.UserSerializer
    )

def filter_users(filter_field, filter_value):
    filtered_data = tools.serialize_filtered_model_objects(
        {filter_field: filter_value},
        User,
        serializers.UserSerializer
    ).data
    return {"users": filtered_data}
