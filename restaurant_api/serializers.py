from django.contrib.auth.models import User

from rest_framework import serializers

from . import models 

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Restaurant
        fields = "__all__"

        
class MenuSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Menu
        fields = "__all__"
        
class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField
    menu = serializers.PrimaryKeyRelatedField
    
    class Meta(object):
        model = models.Vote
        fields = "__all__"
        