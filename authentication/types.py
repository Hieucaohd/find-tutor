import graphene
from graphene_django import DjangoObjectType

from authentication.models import User

from findTutor.models import ImageOfUserModel
from findTutor.types import ImageOfUserType


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
				  )

	imageofusermodel_set = graphene.List(ImageOfUserType, 
										 number_images=graphene.Int(required=False))

	def resolve_imageofusermodel_set(root, info, **kwargs):
		number_images = kwargs.get("number_images", 8)
		return ImageOfUserModel.objects.filter(user=root)[:number_images]
		