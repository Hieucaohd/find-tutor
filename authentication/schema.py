import graphene

from authentication.models import User

from authentication.types import *


class Query(graphene.ObjectType):

	# lấy thông tin của user qua id
	user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))

	def resolve_user_by_id(root, info, **kwargs):
		id = kwargs.get('id')
		return User.objects.get(pk=id)