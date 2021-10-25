from findTutor.models import *
from findTutor.serializers import WaitingTutorSerializer
from findTutor.checkTutorAndParent import isTutor
from findTutor.graphqlQuery import (wating_by_id_query,
                                    tutor_teaching_by_id_query,
                                    parent_room_by_id_query)
from findTutor.messages import RoomNotificationMessage

from authentication.models import User

from websocket.mongoModels import *
from websocket.models import ChannelNameModel
from websocket.groups import GroupName
from websocket.channel_layer_custom import ChannelLayerHandler

import django.dispatch
from django.dispatch import receiver
from django.forms.models import model_to_dict

from asgiref.sync import async_to_sync

import copy

import threading
import multiprocessing

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

######################################## defind the signal ##############################################

parent_create_room_signal = django.dispatch.Signal()
tutor_out_room_signal = django.dispatch.Signal()
parent_invite_tutor_signal = django.dispatch.Signal()

create_tutor_teaching_signal = django.dispatch.Signal()
tutor_not_teaching_room_signal = django.dispatch.Signal()


##########################################################################################################
def image_private_user_model_delete(sender, instance, **kwargs):
    array_item = []

    if instance.avatar:
        old_avatar = OldImagePrivateUserModel()
        old_avatar.image = instance.avatar
        old_avatar.type_image = OldImagePrivateUserModel.type_image_array[0]  # avatar
        array_item.append(old_avatar)

    if instance.identity_card:
        old_identity_card = OldImagePrivateUserModel()
        old_identity_card.image = instance.identity_card
        old_identity_card.type_image = OldImagePrivateUserModel.type_image_array[1]  # identity_card
        array_item.append(old_identity_card)

    if instance.student_card:
        old_student_card = OldImagePrivateUserModel()
        old_student_card.image = instance.student_card
        old_student_card.type_image = OldImagePrivateUserModel.type_image_array[2]  # student_card
        array_item.append(old_student_card)

    for item in array_item:
        item.type_action = OldImagePrivateUserModel.type_action_array[1]
        item.user = instance.user
        item.save()


def image_of_user_model_delete(sender, instance, **kwargs):
    old_image = ImageOfUserModel()
    old_image.image = instance.image
    old_image.user = instance.user
    old_image.type_image = instance.type_image
    old_image.is_public = False
    old_image.is_using = False
    old_image.is_deleted = True
    old_image.save()


def waiting_tutor_model_create(sender, instance, **kwargs):
    # what need to do:
    # - add tutor to room's group
    # - send message to parent
    parent_room = instance.parent_room
    user_of_parent = parent_room.parent.user
    user_of_tutor = instance.tutor.user

    room_group = GroupName.generate_group_name_for_all(instance=parent_room)

    notification_content = {
        "room": parent_room_by_id_query(parent_room),
        "is_new": True,
        "text": RoomNotificationMessage.generate_text(
                    id=RoomNotificationMessage.message_type["tutor_apply_in_room"]["notify_parent"],
                    user_send=user_of_tutor
                ),
    }

    create_thread = threading.Thread

    create_thread(target=ChannelLayerHandler.group_add, kwargs={"user": user_of_tutor,
                                                                "group_name": room_group}).start()

    create_thread(target=ChannelLayerHandler.send, kwargs={"user_send": user_of_tutor,
                                                           "user_receive": user_of_parent,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()

    notify_to_room = wating_by_id_query(instance)
    notify_to_room['type_action'] = "CREATE"
    notify_to_room['type_of_list'] = "waiting_list"
    notify_to_room['type'] = "room.message"

    room_group_realtime = GroupName.generate_group_name_for_realtime(instance=parent_room)
    create_thread(target=async_to_sync(channel_layer.group_send), args=(room_group_realtime, notify_to_room)).start()


def list_invited_model_create(sender, instance, **kwargs):
    # what need to do:
    # - send message to tutor

    parent_room = instance.parent_room
    user_of_tutor = instance.tutor.user
    user_of_parent = parent_room.parent.user

    room_group = GroupName.generate_group_name_for_all(instance=parent_room)

    notification_content = {
        "room": parent_room_by_id_query(parent_room),
        "is_new": True,
        "text": RoomNotificationMessage.generate_text(
                    id=RoomNotificationMessage.message_type["parent_invite_tutor"]["notify_tutor"],
                    user_send=user_of_parent
                ),
    }

    create_thread = threading.Thread

    create_thread(target.NotificationHandler.send, kwargs={"user_send": user_of_parent,
                                                           "user_receive": user_of_tutor,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()
    create_thread(target.NotificationHandler.group_add, kwargs={"user": user_of_tutor,
                                                                "group_name": room_group, }).start()


@receiver(tutor_out_room_signal)
def before_delete_waiting_list_item(sender, **kwargs):
    # what need to do:
    # - discard tutor from room's group
    # - send message to parent
    instance = kwargs.get("instance")
    user_send = kwargs.get("user_send")
    user_receive = kwargs.get("user_receive")

    parent_room = instance.parent_room

    room_group = GroupName.generate_group_name_for_all(instance=parent_room)

    notification_content = {
        "room": parent_room_by_id_query(parent_room),
        "is_new": True,
        "text": kwargs.get("text"),
    }

    create_thread = threading.Thread
    if isTutor(user_send):
        create_thread(target=ChannelLayerHandler.group_discard, kwargs={"user": user_send,
                                                                        "group_name": room_group}).start()

    create_thread(target=ChannelLayerHandler.send, kwargs={"user_send": user_send,
                                                           "user_receive": user_receive,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()


def waiting_tutor_model_delete(sender, instance, **kwargs):
    create_thread = threading.Thread

    parent_room = instance.parent_room
    notify_to_room = {
        "result": {
            "id": instance.id,
        },
        'type_action': "DELETE",
        'type_of_list': "waiting_list",
        'type': "room.message"
    }

    room_group_realtime = GroupName.generate_group_name_for_realtime(instance=parent_room)
    create_thread(target=async_to_sync(channel_layer.group_send), args=(room_group_realtime, notify_to_room)).start()


@receiver(parent_create_room_signal)
def after_parent_create_room(sender, **kwargs):
    # what need to do:
    # - add room's group to FollowModel of parent
    # - add parent's channel name to room's group
    # - notify to people who following parent
    # - save websocket to database

    parent_room = kwargs.get("instance")
    user_of_parent = kwargs.get("info").context.user

    room_group = GroupName.generate_group_name_for_all(instance=parent_room)
    parent_group = GroupName.generate_group_name_for_all(instance=user_of_parent)

    notification_content = {
        "room": parent_room_by_id_query(parent_room),
        "is_new": True,
        "text": RoomNotificationMessage.generate_text(
            id=RoomNotificationMessage.message_type["parent_create_room"]["notify_user_following_parent"],
            user_send=user_of_parent
        ),
    }

    create_thread = threading.Thread

    create_thread(target=ChannelLayerHandler.group_add, kwargs={"user": user_of_parent,
                                                                "group_name": room_group}).start()

    create_thread(target=ChannelLayerHandler.group_send, kwargs={"user_send": user_of_parent,
                                                                 "group_name": parent_group,
                                                                 "content": notification_content,
                                                                 "save_to_model": RoomNotificationModel}).start()


@receiver(create_tutor_teaching_signal)
def after_create_tutor_teaching(sender, **kwargs):
    # what need to do:
    # - notify to room's group
    user_send = kwargs.get("user_send")
    user_receive = kwargs.get("user_receive")
    instance = kwargs.get("instance")

    parent_room = instance.parent_room
    room_group = GroupName.generate_group_name_for_all(instance=parent_room)

    notification_content = {
        "room": parent_room_by_id_query(parent_room),
        "is_new": True,
        "text": kwargs.get("text"),
    }

    notification_content_for_room = copy.deepcopy(notification_content)
    notification_content_for_room["text"] = RoomNotificationMessage.generate_text(
        id=RoomNotificationMessage.message_type["room_has_tutor_teaching"]["notify_tutors_in_waiting_list_and_invited_list"],
        user_send=user_send,
    )

    create_thread = threading.Thread

    create_thread(target=ChannelLayerHandler.send, kwargs={"user_send": user_send,
                                                           "user_receive": user_receive,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()

    create_thread(target=ChannelLayerHandler.group_send_except, kwargs={"user_send": parent_room.parent.user,
                                                                        "group_name": room_group,
                                                                        "content": notification_content_for_room,
                                                                        "save_to_model": RoomNotificationModel,
                                                                        "except_users": [user_send,
                                                                                         user_receive]}).start()


def tutor_teaching_model_create(sender, instance, **kwargs):
    create_thread = threading.Thread

    parent_room = instance.parent_room
    notify_to_room = tutor_teaching_by_id_query(instance)
    notify_to_room['type_action'] = "CREATE"
    notify_to_room['type_of_list'] = "tutor_teaching"
    notify_to_room['type'] = "room.message"

    room_group_realtime = GroupName.generate_group_name_for_realtime(instance=parent_room)
    create_thread(target=async_to_sync(channel_layer.group_send), args=(room_group_realtime, notify_to_room)).start()


@receiver(tutor_not_teaching_room_signal)
def after_delete_tutor_from_teaching(sender, **kwargs):
    # what need to do:
    # - notify to room's group
    user_send = kwargs.get("user_send")
    user_receive = kwargs.get("user_receive")
    instance = kwargs.get("instance")

    parent_room = instance.parent_room
    room_group = GroupName.generate_group_name_for_all(instance=parent_room)

    notification_content = {
        "room": parent_room_by_id_query(parent_room),
        "is_new": True,
        "text": kwargs.get("text"),
    }

    notification_content_for_room = copy.deepcopy(notification_content)
    notification_content_for_room["text"] = RoomNotificationMessage.generate_text(
        id=RoomNotificationMessage.message_type["room_expired_with_tutor_teaching"]["notify_tutors_in_waiting_list_and_invited_list"],
        user_send=user_send
    )

    create_thread = threading.Thread

    create_thread(target=ChannelLayerHandler.send, kwargs={"user_send": user_send,
                                                           "user_receive": user_receive,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()

    create_thread(target=ChannelLayerHandler.group_send_except, kwargs={"user_send": parent_room.parent.user,
                                                                        "group_name": room_group,
                                                                        "content": notification_content_for_room,
                                                                        "save_to_model": RoomNotificationModel,
                                                                        "except_users": [user_send,
                                                                                         user_receive]}).start()


def tutor_teaching_model_delete(sender, instance, **kwargs):
    create_thread = threading.Thread

    parent_room = instance.parent_room
    notify_to_room = {"result": {
        "id": instance.id,
    }, 'type_action': "DELETE", 'type_of_list': "tutor_teaching", 'type': "room.message"}

    room_group_realtime = GroupName.generate_group_name_for_realtime(instance=parent_room)
    create_thread(target=async_to_sync(channel_layer.group_send), args=(room_group_realtime, notify_to_room)).start()
