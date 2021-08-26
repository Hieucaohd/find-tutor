from django.db import models

from findTutor.models import TutorModel, ParentModel, ParentRoomModel
from authentication.models import User

class CommentAboutUserModel(models.Model):
	about_who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='about_user')
	belong_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer_user')
	create_at = models.DateTimeField(auto_now_add=True)
	content = models.TextField(null=False, blank=False)


class CommentAboutParentRoomModel(models.Model):
	about_who = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)
	belong_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	create_at = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
