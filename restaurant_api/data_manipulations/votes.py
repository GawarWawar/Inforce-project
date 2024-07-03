from rest_framework import status

from restaurant_api import serializers, models
from . import tools


def get_all_votes():
    """
        Vrapper of function serialize_filtered_model_objects with specified model and serializer
    """
    all_votes = tools.serialize_filtered_model_objects(
        {"all": True},
        models.Vote,
        serializers.VoteSerializer
    )
    return {"votess": all_votes.data}

def post_vote(request_data):
    """
        Validate vote through Serializer and return it or details
    """
    new_vote = serializers.VoteSerializer(data = request_data)
    if new_vote.is_valid():
        new_vote.save()
        
        return {"vote": new_vote.data}
    else:
        return {"details": new_vote.errors, "status": status.HTTP_400_BAD_REQUEST}

def get_vote_by_id(vote_id):
    """
        Vrapper of function get_object_by_id with specified object_name_string, model and serializer
    """
    return tools.get_object_by_id(vote_id, "vote",models.Vote, serializers.VoteSerializer)

def update_vote_by_id(request_data, vote_id):
    """
        Vrapper of function update_object with specified object_name_string, model and serializer
    """    
    return tools.update_object(
        request_data, vote_id, "vote", models.Vote, serializers.VoteSerializer
    )
    
def filter_votes(filter_field, filter_value):
    """
        Vrapper of function serialize_filtered_model_objects with specified object_name_string, model and serializer
    """
    filtered_data = tools.serialize_filtered_model_objects(
        {filter_field: filter_value},
        models.Vote,
        serializers.VoteSerializer
    ).data
    return {"votes": filtered_data}