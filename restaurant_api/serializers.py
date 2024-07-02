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
    class Meta(object):
        model = Vote
        fields = "__all__"
        