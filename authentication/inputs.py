import graphene

class LinkInput(graphene.InputObjectType):
	url = graphene.String(required=True)
	image = graphene.String(required=False)
	name = graphene.String(required=False)