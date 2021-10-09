import graphene

from authentication.inputs import *
from authentication.models import *
from authentication.types import *


class CreateLinkMutation(graphene.Mutation):
	class Arguments:
		input_fields = LinkInput(required=True)

	link = graphene.Field(LinkType)

	@classmethod
	def mutate(cls, root, info, input_fields):
		user = info.context.user
		if not user.is_authenticated:
			raise Exception("user chua dang nhap")
		link = LinkModel.objects.create(user=user,
										url=input_fields.url,
										name=input_fields.name,
										image=input_fields.image)

		return CreateLinkMutation(link=link)