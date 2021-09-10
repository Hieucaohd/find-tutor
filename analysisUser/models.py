from django.db import models

from authentication.models import User

# Create your models here.
class UserSearchModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	type_user = models.CharField(max_length=200, null=True, blank=True)

	content_search = models.TextField(null=False, blank=False)

	create_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"'{self.user.email}' type: '{self.type_user}', search: '{self.content_search}', at: '{self.create_at}'"