from findTutor.models import *

from authentication.models import User

from notification.mongoModels import *
from notification.models import ChannelNameModel
from notification.groups import GroupName, NotificationHandler

import django.dispatch
from django.dispatch import receiver

from asgiref.sync import async_to_sync

import copy

import threading
import multiprocessing

from findTutor.checkTutorAndParent import isTutor

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


######################################## defind the signal ##############################################

parent_create_room_signal = django.dispatch.Signal()
tutor_out_room = django.dispatch.Signal()
parent_invite_tutor = django.dispatch.Signal()

create_tutor_teaching = django.dispatch.Signal()



##########################################################################################################
def before_image_private_user_delete(sender, instance, **kwargs):
    array_item = []

    if instance.avatar:
        old_avatar = OldImagePrivateUserModel()
        old_avatar.image = instance.avatar
        old_avatar.type_image = OldImagePrivateUserModel.type_image_array[0]    # avatar
        array_item.append(old_avatar)

    if instance.identity_card:
        old_identity_card = OldImagePrivateUserModel()
        old_identity_card.image = instance.identity_card
        old_identity_card.type_image = OldImagePrivateUserModel.type_image_array[1] # identity_card
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


def before_image_of_user_delete(sender, instance, **kwargs):
    old_image = ImageOfUserModel()
    old_image.image = instance.image
    old_image.user = instance.user
    old_image.type_image = instance.type_image
    old_image.is_public = False
    old_image.is_using = False
    old_image.is_deleted = True
    old_image.save()


def after_create_waiting_list_item(sender, instance, **kwargs):
	# what need to do:
    # - add tutor to room's group
    # - send message to parent
    parent_room = instance.parent_room
    user_of_parent = parent_room.parent.user
    user_of_tutor = instance.tutor.user

    room_group = GroupName.generate_group_name_for_all(parent_room)

    notification_content = {
        "room_id": parent_room.id,
        "content": f"gia sư {user_of_tutor.tutormodel.full_name} đã ứng tuyển vào lớp {parent_room.subject} {parent_room.lop} của bạn",
    }

    create_thread = threading.Thread

    create_thread(target=NotificationHandler.group_add, kwargs={"user": user_of_tutor,
                                                                "group_name": room_group}).start()

    create_thread(target=NotificationHandler.send, kwargs={"user_send": user_of_tutor,
                                                           "user_receive": user_of_parent,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()


def after_create_invited_item(sender, instance, **kwargs):
    # what need to do:
    # - send message to tutor

    parent_room = instance.parent_room
    user_of_tutor = instance.tutor.user
    user_of_parent = parent_room.parent.user

    room_group = GroupName.generate_group_name_for_all(parent_room)

    notification_content = {
        "room_id": parent_room.id,
        "content": f"phụ huynh {user_of_parent.parentmodel.full_name} đã mời bạn dạy lớp {parent_room.subject} {parent_room.lop}"
    }

    create_thread = threading.Thread

    create_thread(target.NotificationHandler.send, kwargs={"user_send": user_of_parent,
                                                           "user_receive": user_of_tutor,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()


@receiver(tutor_out_room)
def before_delete_waiting_list_item(sender, **kwargs):
    # what need to do:
    # - discard tutor from room's group
    # - send message to parent
    instance = kwargs.get("instance")
    user_send = kwargs.get("user_send")
    user_receive = kwargs.get("user_receive")

    parent_room = instance.parent_room

    room_group = GroupName.generate_group_name_for_all(parent_room)

    notification_content = {
        "room_id": parent_room.id,
        "content": kwargs.get("content"),
    }

    create_thread = threading.Thread
    if isTutor(user_send):
        create_thread(target=NotificationHandler.group_discard, kwargs={"user": user_send,
                                                                        "group_name": room_group}).start()

    create_thread(target=NotificationHandler.send, kwargs={"user_send": user_send,
                                                           "user_receive": user_receive,
                                                           "content": notification_content,
                                                           "save_to_model": RoomNotificationModel}).start()

    


@receiver(parent_create_room_signal)
def after_parent_create_room(sender, **kwargs):
    # what need to do:
    # - add room's group to FollowModel of parent
    # - add parent's channel name to room's group
    # - notify to people who following parent
    # - save notification to database

    parent_room = kwargs.get("instance")
    user_of_parent = kwargs.get("info").context.user

    room_group = GroupName.generate_group_name_for_all(parent_room)
    parent_group = GroupName.generate_group_name_for_all(user_of_parent)

    notification_content = {
        "room_id": parent_room.id,
        "content": f"phụ huynh {user_of_parent.parentmodel.full_name} đã tạo lớp {parent_room.subject} {parent_room.lop}. Hãy ứng tuyển ngay nào!",
    }

    create_thread = threading.Thread

    create_thread(target=NotificationHandler.group_add, kwargs={"user": user_of_parent, 
                                                                "group_name": room_group}).start()

    create_thread(target=NotificationHandler.group_send, kwargs={"user_send": user_of_parent, 
                                                                 "group_name": parent_group, 
                                                                 "content": notification_content,
                                                                 "save_to_model": RoomNotificationModel}).start()


@receiver(create_tutor_teaching)
def after_create_tutor_teaching(sender, **kwargs):
    # what need to do:
    # - notify to room's group
    user_send = kwargs.get("user_send")
    user_receive = kwargs.get("user_receive")
    instance = kwargs.get("instance")

    parent_room = instance.parent_room
    room_group = GroupName.generate_group_name_for_all(parent_room)

    notification_content = {
        "room_id": parent_room.id,
        "content": kwargs.get("content"),
    }

    create_thread = threading.Thread

    create_thread(target=NotificationHandler.group_send, kwargs={"user_send": user_send,
                                                                 "group_name": room_group,
                                                                 "content": notification_content,
                                                                 "save_to_model": RoomNotificationModel}).start()