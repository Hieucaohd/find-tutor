import graphene

import findTutor.schema
import search.schema
import authentication.schema


class Query(findTutor.schema.Query, 
			search.schema.Query, 
			authentication.schema.Query, 
			graphene.ObjectType):
	pass


class Mutation(findTutor.schema.Mutation, 
			   graphene.ObjectType):
	pass


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
