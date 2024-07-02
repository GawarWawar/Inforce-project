from rest_framework import status

from restaurant_api import serializers, models
from . import tools


def get_all_votes():
    all_votes = tools.serialize_filtered_model_objects(
        {"all": True},
        models.Vote,
        serializers.VoteSerializer
    )
    return {"menus": all_votes.data}

def get_vote_by_id(vote_id):
    return tools.get_object_by_id(vote_id, "vote",models.Vote, serializers.VoteSerializer)

def update_vote_by_id(request_data, vote_id):
    return tools.update_object(
        request_data, vote_id, "vote", models.Vote, serializers.VoteSerializer
    )

def post_vote(request_data):
    new_vote = serializers.VoteSerializer(data = request_data)
    if new_vote.is_valid():
        new_vote.save()
        
        return {"menu": new_vote.data}
    else:
        return {"errors": new_vote.errors, "status": status.HTTP_400_BAD_REQUEST}
    
def filter_votes(filter_field, filter_value):
    filtered_data = tools.serialize_filtered_model_objects(
        {filter_field: filter_value},
        models.Vote,
        serializers.VoteSerializer
    ).data
    return {"votes": filtered_data}