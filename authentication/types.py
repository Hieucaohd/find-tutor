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
    number_image_of_user = graphene.Int()

    def resolve_number_image_of_user(root, info, **kwargs):
        return ImageOfUserModel.objects.filter(user=root).count()

    imageofusermodel_set = graphene.List(ImageOfUserType, 
                                         number_images=graphene.Int(required=False))

    def resolve_imageofusermodel_set(root, info, **kwargs):
        number_images = kwargs.get("number_images", 8)
        return ImageOfUserModel.objects.filter(user=root)[:number_images]

    first_name = graphene.String()

    def resovle_first_name(root, info, **kwargs):
        if hasattr(root, "tutormodel"):
            return root.tutormodel.first_name

        if hasattr(root, "parentmodel"):
            return root.parentmodel.first_name

    last_name = graphene.String()

    def resolve_last_name(root, info, **kwargs):
        if hasattr(root, "tutormodel"):
            return root.tutormodel.last_name

        if hasattr(root, "parentmodel"):
            return root.parentmodel.last_name
        
