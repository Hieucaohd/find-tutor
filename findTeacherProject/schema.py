import graphene

import findTutor.schema
import search.schema
import authentication.schema
import websocket.schema


class Query(findTutor.schema.Query,
            search.schema.Query,
            authentication.schema.Query,
            websocket.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(findTutor.schema.Mutation,
               authentication.schema.Mutation, 
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)


