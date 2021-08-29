from django.db.models.signals import pre_delete
from .models import ImagePrivateUserModel, OldImagePrivateUserModel


def before_image_private_user_delete(sender, instance, **kwargs):
	old_avatar = OldImagePrivateUserModel()
	old_identity_card = OldImagePrivateUserModel()
	old_student_card = OldImagePrivateUserModel()

	old_avatar.type_image = 1
	old_identity_card.type_image = 2
	old_student_card = 3

	old_avatar.user = instance.user
	old_identity_card.user = instance.user
	old_student_card = instance.user

	old_avatar.image = instance.avatar
	old_identity_card.image = instance.identity_card
	old_student_card.image = instance.student_card

	old_avatar.save()
	old_identity_card.save()
	old_student_card.save()

	print("ban luu thanh cong")

pre_delete.connect(before_image_private_user_delete, connect=ImagePrivateUserModel)


