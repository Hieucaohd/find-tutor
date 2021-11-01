from channels.layers import get_channel_layer

from websocket.mongoModels import *
from websocket.models import ChannelNameModel

from authentication.models import User

from findTutor.models import ParentRoomModel

from asgiref.sync import async_to_sync


class GroupName:
    
    @staticmethod
    def generate_group_name_for_all(instance):
        model_name = instance.__class__.__name__
        id = instance.id
        return f"{model_name}.{id}.all"

    @staticmethod
    def generate_group_name_for_info(instance):
        model_name = instance.__class__.__name__
        id = instance.id
        return f"{model_name}.{id}.info"

    @staticmethod
    def generate_group_name_for_realtime(id=None, model=None, instance=None):
        if model: 
            model_name = model.__name__

        if instance:
            id = instance.id
            model_name = instance.__class__.__name__
        return f"{model_name}.{id}.realtime"

    @staticmethod
    def decode_from_group_name(group_name):
        model_name, id, prefix = group_name.split(".")
        return {
            "model_name": model_name,
            "id": int(id),
            "prefix": prefix,
        }











