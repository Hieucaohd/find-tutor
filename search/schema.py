import graphene

from graphql_jwt.decorators import login_required

from findTutor.models import *
from findTutor.types import *

from search.resolveSearch import ResolveSearchForRoom, ResolveSearchForTutor, ResolveSearchForParent
from search.mongoModels import SearchRoomModel, SearchTutorModel, SearchParentModel

import copy

from findTeacherProject.paginator import paginator_sql_query


class ResultSearchRoomType(graphene.ObjectType):
    result = graphene.List(ParentRoomType)
    num_pages = graphene.Int()

class ResultSearchTutorType(graphene.ObjectType):
    result = graphene.List(TutorType)
    num_pages = graphene.Int()

class ResultSearchParentType(graphene.ObjectType):
    result = graphene.List(ParentType)
    num_pages = graphene.Int()


def save_search_to_mongo(request, model, kwargs, take_result=False):
    if request.user.is_authenticated:
        data_search = copy.deepcopy(kwargs)
        if kwargs.get("page"):
            del data_search["page"]

        if kwargs.get("num_in_page"):
            del data_search["num_in_page"]

        model(user_id=request.user.id, content_search=data_search).create(take_result)


class Query(graphene.ObjectType):

    # tim kiem lop hoc
    search_room = graphene.Field(ResultSearchRoomType, province_code  = graphene.Int(required=False),
                                                   district_code  = graphene.Int(required=False),
                                                   ward_code      = graphene.Int(required=False),
                                                   lop            = graphene.List(graphene.Int, required=False),
                                                   price          = graphene.List(graphene.Int, required=False),
                                                   sex_of_teacher = graphene.String(required=False),
                                                   type_teacher   = graphene.List(graphene.String, required=False),
                                                   search_infor   = graphene.String(required=False),
                                                   order_by       = graphene.String(required=False),


                                                   # phan trang
                                                   page           = graphene.Int(required=False), 
                                                   num_in_page    = graphene.Int(required=False),
                              token=graphene.String(required=False),
                                )

    def resolve_search_room(root, info, **kwargs):
        page = kwargs.get("page", 1)
        num_in_page = kwargs.get("num_in_page", 16)

        request = info.context

        save_search_to_mongo(request=request, model=SearchRoomModel, kwargs=kwargs, take_result=False)

        def fields(item):
            return [item.subject, item.other_require]
        
        kwargs['request'] = request

        search_room = ResolveSearchForRoom(model=ParentRoomModel, fields=fields, kwargs=kwargs)

        result = paginator_sql_query(list(search_room.resolve_search()), num_in_page, page)

        return {
            'result': result,
            'num_pages': result.paginator.num_pages
        }


    # tim kiem gia su
    search_tutor = graphene.Field(ResultSearchTutorType, province_code = graphene.Int(required=False),
                                                     district_code = graphene.Int(required=False),
                                                     ward_code     = graphene.Int(required=False),
                                                     lop           = graphene.List(graphene.Int, required=False),
                                                     search_infor  = graphene.String(required=False),

                                                     # phan trang
                                                     page          = graphene.Int(required=False), 
                                                     num_in_page   = graphene.Int(required=False),

                              token=graphene.String(required=False),
                                )

    def resolve_search_tutor(root, info, **kwargs):
        page = kwargs.get("page", 1)
        num_in_page = kwargs.get("num_in_page", 16)

        save_search_to_mongo(request=info.context, model=SearchTutorModel, kwargs=kwargs, take_result=False)

        def fields(item):
            return [item.full_name, item.experience, item.achievement, item.university, item.profession]

        search_tutor = ResolveSearchForTutor(model=TutorModel, fields=fields, kwargs=kwargs)

        result = paginator_sql_query(list(search_tutor.resolve_search()), num_in_page, page)

        return {
            'result': result,
            'num_pages': result.paginator.num_pages
        }


    # tim kiem phu huynh
    search_parent = graphene.Field(ResultSearchParentType, province_code = graphene.Int(required=False),
                                                       district_code = graphene.Int(required=False),
                                                       ward_code     = graphene.Int(required=False),
                                                       search_infor  = graphene.String(required=False),

                                                       # phan trang
                                                       page          = graphene.Int(required=False), 
                                                       num_in_page   = graphene.Int(required=False),
                              token=graphene.String(required=False),
                                )

    def resolve_search_parent(root, info, **kwargs):
        page = kwargs.get("page", 1)
        num_in_page = kwargs.get("num_in_page", 16)

        save_search_to_mongo(request=info.context, model=SearchParentModel, kwargs=kwargs, take_result=False)

        def fields(item):
            return [item.full_name]

        search_parent = ResolveSearchForParent(model=ParentModel, fields=fields, kwargs=kwargs)

        result = paginator_sql_query(list(search_parent.resolve_search()), num_in_page, page)

        return {
            'result': result,
            'num_pages': result.paginator.num_pages
        }
