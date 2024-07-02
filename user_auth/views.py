from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer
from . import tokens
from .data_manipulations import users as dm_users

@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        
        generated_tokens = tokens.create_jwt_pair_for_user(user)
        data = serializer.data
        data.pop("password")
        return Response({"tokens": generated_tokens, "user": data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
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

@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(["GET"])
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

@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(["GET", "PUT"])
def users_by_id(request, user_id):
    if request.method == "GET": 
        particular_user = dm_users.get_user_by_id(user_id)
        if 'errors' in particular_user:
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
        