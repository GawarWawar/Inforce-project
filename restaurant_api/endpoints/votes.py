import datetime
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from restaurant_api.data_manipulations import restaurants as dm_restaurants
from restaurant_api.data_manipulations import menus as dm_menus
from restaurant_api.data_manipulations import votes as dm_votes

@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def votes(request):
    if request.method == "GET": 
        return Response(dm_votes.get_all_votes())
    elif request.method == "POST":
        response = dm_votes.post_vote(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)

@api_view(["GET", "PUT"])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])        
def votes_by_id(request, vote_id):
    if request.method == "GET": 
        particular_vote = dm_votes.get_vote_by_id(vote_id)
        if 'details' in particular_vote:
            response_status = particular_vote.pop("status")
            return Response(particular_vote, status=response_status)
        else:
            return Response(particular_vote.pop("vote"))
        
    if request.method == "PUT":
        response = dm_votes.update_vote_by_id(request.data, vote_id)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)

@api_view(["GET"])      
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def votes_filter_by_field_and_value(request, filter_field, filter_value):
    if request.method == "GET":
        return Response(dm_votes.filter_votes(filter_field, filter_value))
    
@api_view(["GET"])      
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def votes_calculate_for_today(request):
    if request.method == "GET":
        
        results = dm_menus.filter_menus("day_created", datetime.date.today())["menus"]
        
        for menu in results:
            menu["votes_count"] = len(dm_votes.filter_votes("menu", menu["id"])["votes"])
        
        response = {"restaurants": []}
        for menu in results:
            response["restaurants"].append(
                {
                    "restaurant": menu["restaurant"],
                    "menu": menu["id"],
                    "votes_count": menu["votes_count"]
                }
            )
        return Response(response)