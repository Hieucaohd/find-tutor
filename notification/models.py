from django.db import models

from authentication.models import User

from findTutor.models import ParentRoomModel

# Create your models here.


class NotificationWhenCreateRoomModel(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	receiver = models.ForeignKey(User, on_delete=models.CASCADE)

	create_at = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)

	text_preview = models.CharField(max_length=100)
	room = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)


class NotificationWhenCommentInTutorInforModel(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	receiver = models.ForeignKey(User, on_delete=models.CASCADE)

	create_at = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)

	text_preview = models.CharField(max_length=100)

	# comment = 