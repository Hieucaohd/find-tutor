from django.db import models

from authentication.models import User
# Create your models here.


class SearchModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	content_search = models.TextField()

	create_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.content_search) + ". Create at: " + str(self.create_at)
