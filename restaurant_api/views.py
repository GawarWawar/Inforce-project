from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from . import serializers, models

@api_view(["GET", "POST"])
def restourants(request):
    if request.method == "GET": 
        all_restourants = models.Restourant.objects.all()
        all_restourants = serializers.RestourantSerializer(all_restourants, many = True)
        return Response({"restourants": all_restourants.data})
    
    elif request.method == "POST":
        new_resourant = serializers.RestourantSerializer(data = request.data)
        if new_resourant.is_valid():
            new_resourant.save()
            restourant = models.Restourant.objects.get(name = request.data["name"])
            
            return Response({"restourant": new_resourant.data})
        else:
            return Response(new_resourant.errors, status=status.HTTP_400_BAD_REQUEST)
        
