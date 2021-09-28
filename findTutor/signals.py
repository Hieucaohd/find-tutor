from findTutor.models import *
from notification.mongoModels import *
from notification.groups import GroupName

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


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
	# notify here
    # notify for parent

	pass



