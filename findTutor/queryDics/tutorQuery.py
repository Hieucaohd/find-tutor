import graphene
from graphene_django import DjangoObjectType
from ..models import TutorModel

class TutorType(DjangoObjectType):
	class Meta:
		model = TutorModel

class Query(graphene.ObjectType):
	pass