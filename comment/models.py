from django.db import models

from findTutor.models import TutorModel, ParentModel, ParentRoomModel
from authentication.models import User

# Create your models here.


class CommentBaseMode:
	about_who = None
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	create_at = models.DateTimeField(auto_now_add=True)
	content = models.TextField()


class CommentAboutTutorModel(models.Model, CommentBaseMode):
	about_who = models.ForeignKey(TutorModel, on_delete=models.CASCADE)


class CommentAboutParentModel(models.Model, CommentBaseMode):
	about_who = models.ForeignKey(ParentModel, on_delete=models.CASCADE)


class CommentAboutParentRoomModel(models.Model, CommentBaseMode):
	about_who = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)
