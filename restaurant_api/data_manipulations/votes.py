from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest, Http404

from restaurant_api import serializers, models
from . import tools


def get_all_votes():
    all_votes = tools.serialize_filtered_model_objects(
        {"all": True},
        models.Vote,
        serializers.VoteSerializer
    )
    return {"menus": all_votes.data}

def post_vote(request_data):
    new_vote = serializers.VoteSerializer(data = request_data)
    if new_vote.is_valid():
        new_vote.save()
        
        return {"menu": new_vote.data}
    else:
        return {"errors": new_vote.errors, "status": status.HTTP_400_BAD_REQUEST}