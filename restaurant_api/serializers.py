from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Restaurant, Menu, Vote

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Restaurant
        fields = "__all__"

        
class MenuSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Menu
        fields = "__all__"
        
class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField
    menu = serializers.PrimaryKeyRelatedField
    
    class Meta(object):
        model = Vote
        fields = "__all__"
        