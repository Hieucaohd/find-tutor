from channels.layers import get_channel_layer

from notification.mongoModels import *
from notification.models import ChannelNameModel

from authentication.models import User

from findTutor.models import ParentRoomModel

from asgiref.sync import async_to_sync


class GroupName:
    
    @staticmethod
    def generate_group_name_for_all(instance):
        model_name = instance.__class__.__name__
        id = instance.id
        return f"{model_name}.{id}.notify"

    @staticmethod
    def generate_group_name_for_master(instance):
        model_name = instance.__class__.__name__
        id = instance.id
        return f"{model_name}.{id}.master_notify"

channel_layer = get_channel_layer()

class NotificationHandler:
    def __init__(self):
        # function of this class:
        # - send notification to a group and 
        #   save notification to database of the members of this group
        # - add a user's channel name to a group (save to database)
        pass

    @staticmethod
    def group_send(user_send, group_name, content, save_to_model):
        if not isinstance(content, dict):
            raise Exception("content is not a dictionary")

        if not isinstance(user_send, User):
            raise Exception("user is not object of User model")

        # send to group
        content['user_id_send'] = user_send.id
        content['type'] = "notify.message"
        async_to_sync(channel_layer.group_send)(group_name, content)

        # save to database
        members = FollowModel().collection.find({ 
            "following_groups": {
                "$all": [group_name]
            } 
        })

        for member in members:
            notification_content['user_id_receive'] = member["user_id"]
            save_to_model(**content).create(take_result=False)

    @staticmethod
    def group_add(user, group_name):
        if not isinstance(user, User):
            raise Exception("user is not object of User model")

        channel_names = ChannelNameModel.objects.filter(user = user)
        for channel_name in channel_names:
            async_to_sync(channel_layer.group_add)(channel_name.channel_name, group_name)

        follow_model_collection = FollowModel().collection
        follow_model_collection.find_one_and_update({ "user_id": user.id }, { 
            "$addToSet": { 
                "following_groups":  group_name,
            }
        }, upsert=True)

    @staticmethod
    def group_discard(user, group_name):
        if not isinstance(user, User):
            raise Exception("user is not object of User model")

        # remove user's channel name from group
        channel_names = ChannelNameModel.objects.filter(user = user)
        for channel_name in channel_names:
            async_to_sync(channel_layer.group_discard)(channel_name.channel_name, group_name)

        # remove group name from database of user
        follow_model_collection = FollowModel().collection
        follow_model_collection.update({ "user_id": user.id }, {
            "$pull": {
                "following_groups": group_name,
            }
        })

    @staticmethod
    def send(user_send, user_receive, content, save_to_model):
        if not (isinstance(user_send, User) and isinstance(user_receive, User)):
            raise Exception("user is not object of User model")

        content['user_id_send'] = user_send.id
        content['user_id_receive'] = user_receive.id
        content['type'] = "notify.message"

        # send notification
        channel_names = ChannelNameModel.objects.filter(user = user_receive)
        for channel_name in channel_names:
            async_to_sync(channel_layer.send)(channel_name.channel_name, content)

        # save to database
        save_to_model(**content).create(take_result=False)











