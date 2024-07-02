from rest_framework import serializers

from .models import Restourant, Menu, Vote

class RestourantSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Restourant
        fields = "__all__"

        
class MenuSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Menu
        fields = "__all__"
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Vote
        fields = "__all__"
        