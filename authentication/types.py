from graphene_django import DjangoObjectType
from authentication.models import User

class UserType(DjangoObjectType):
	class Meta:
		model = User
		fields = (
				  "id",
				  "username",
				  "tutormodel",
				  "parentmodel",
				  "imageprivateusermodel",
				  "oldimageprivateusermodel_set",
				  "imageofusermodel_set",
				  )