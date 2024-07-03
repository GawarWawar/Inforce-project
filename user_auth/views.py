from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, AnonymousUser

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer
from . import tokens
from .data_manipulations import users as dm_users

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    response = dm_users.post_user(request.data)
    if "error" in response:
        response_status = response.pop("status")
        return Response(response, status=response_status)
    else:
        return Response(response)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login(request):
    user = get_object_or_404(User, username = request.data["username"])
    
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST) 
    generated_tokens = tokens.create_jwt_pair_for_user(user)
    serializer = UserSerializer(user)
    data = serializer.data
    data.pop("password")
    return Response({"tokens": generated_tokens, "user": data})

@api_view(["GET"])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_token(request):
    serializer = UserSerializer(request.user)
    data = serializer.data
    data.pop("password")
    return Response(f"User authenticated: {data} ")

@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def users(request):
    if request.method == "GET": 
        return Response(dm_users.get_all_users())
    elif request.method == "POST":    
        response = dm_users.post_user(request.data)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)

@api_view(["GET", "PUT"])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def users_by_id(request, user_id):
    if request.method == "GET": 
        particular_user = dm_users.get_user_by_id(user_id)
        if 'details' in particular_user:
            response_status = particular_user.pop("status")
            return Response(particular_user, status=response_status)
        else:
            return Response(particular_user.pop("user"))
        
    if request.method == "PUT":
        response = dm_users.update_vote_by_id(request.data, user_id)
        if "error" in response:
            response_status = response.pop("status")
            return Response(response, status=response_status)
        else:
            return Response(response)
        