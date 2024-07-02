from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def create_jwt_pair_for_user(user):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access": str(refresh.access_token), 
        "refresh": str(refresh)
    }

    return tokens

def generate_new_acess_token(user):
    refresh = AccessToken.for_user(user)
    tokens = {
        "access": str(refresh), 
    }

    return tokens