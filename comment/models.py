from django.db import models

from findTutor.models import TutorModel, ParentModel, ParentRoomModel
from authentication.models import User

# Create your models here.


class CommentAboutTutorModel(models.Model):
	about_who = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
	belong_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	create_at = models.DateTimeField(auto_now_add=True)
	content = models.TextField(null=False)
	

class CommentAboutParentModel(models.Model):
	about_who = models.ForeignKey(ParentModel, on_delete=models.CASCADE)
	belong_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	create_at = models.DateTimeField(auto_now_add=True)
	content = models.TextField()


class CommentAboutParentRoomModel(models.Model):
	about_who = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)
	belong_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	create_at = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
