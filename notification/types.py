# import graphene

# from authentication.types import UserType
# from authentication.models import User

# from notification.mongoModels import *


# class FriendType(graphene.ObjectType):
#     list_friend = graphene.List(UserType, user_id=graphene.ID(required=True))

#     def resolve_list_friend(root, info, **kwargs):
#         user_id = kwargs.get("user_id", 0)
#         list_friend_ids = FriendModel().get(user_id=user_id).list_friends
#         return User.objects.filter(id__in = list_friend_ids)


# class RoomNotificationType(graphene.ObjectType):
#     user_id_send = graphene.ID()
#     user_id_receive = graphene.ID()
#     is_seen = graphene.Boolean()
#     room = graphene.ObjectType()
#     text = graphene.String()


# class FollowType(graphene.ObjectType):
#     user_id = graphene.ID()
#     following_groups = graphene.List(graphene.String)