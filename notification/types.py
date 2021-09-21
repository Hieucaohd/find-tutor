import graphene

from authentication.types import UserType
from authentication.models import User

from mongoModels import *


class FriendType(graphene.ObjectType):
    list_friend = graphene.List(UserType, user_id=graphene.ID(required=True))

    def resolve_list_friend(root, info, **kwargs):
        user_id = kwargs.get("user_id", 0)
        list_friend_ids = FriendModel().get(user_id=user_id).list_friends
        return User.objects.filter(id__in = list_friend_ids)
