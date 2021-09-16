import graphene

from graphql_jwt.decorators import login_required

from findTutor.paginator import paginator_function

from findTutor.types import *
from findTutor.models import *
from findTutor.mutations import *

from django.db.models import Q

from .checkTutorAndParent import isTutor


class Query(graphene.ObjectType):

    # lấy danh sach các lớp học
    all_room = graphene.Field(ResultAllRoom, page=graphene.Int(required=False), num_in_page=graphene.Int(required=False))

    def resolve_all_room(root, info, **kwargs):
        page = kwargs.get("page", 1)
        num_in_page = kwargs.get("num_in_page", 16)

        query_set = ParentRoomModel.objects.all()

        request = info.context
        if isTutor(request.user):
            print("ban la tutor")
        if (request.user.is_authenticated) and isTutor(request.user):
            user_not_in_list = (~Q(waitingtutormodel__tutor__user=request.user) & 
                                ~Q(listinvitedmodel__tutor__user=request.user) &
                                ~Q(tryteachingmodel__tutor__user=request.user) &
                                ~Q(tutorteachingmodel__tutor__user=request.user)
                                )
            query_set = query_set.filter(user_not_in_list)

        print(query_set.count())
        result = paginator_function(query_set, num_in_page, page)

        return {
            'result': result,
            'num_pages': result.paginator.num_pages
        }


    # lay room thong qua id
    room_by_id = graphene.Field(ParentRoomType, id=graphene.Int(required=True))

    def resolve_room_by_id(root, info, **kwargs):
        id = kwargs.get('id')
        return ParentRoomModel.objects.get(pk=id)


    # lay danh sach cac tutor
    all_tutor = graphene.Field(ResultAllTutor, page=graphene.Int(required=False), num_in_page=graphene.Int(required=False))

    def resolve_all_tutor(root, info, **kwargs):
        page = kwargs.get("page", 1)
        num_in_page = kwargs.get("num_in_page", 16)

        result = paginator_function(TutorModel.objects.all(), num_in_page, page)

        return {
            'result': result,
            'num_pages': result.paginator.num_pages
        }


class Mutation(graphene.ObjectType):
    create_parent_room = CreateParentRoomMutation.Field()
