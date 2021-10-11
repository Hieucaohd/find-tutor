import graphene

from graphql_jwt.decorators import login_required

from findTutor.paginator import paginator_function

from findTutor.types import *
from findTutor.models import *
from findTutor.mutations import *

from django.db.models import Q

from .checkTutorAndParent import isTutor, isParent


class Query(graphene.ObjectType):

    # lấy danh sach các lớp học
    all_room = graphene.Field(ResultAllRoom, 
                              token=graphene.String(required=False),
                              page=graphene.Int(required=False), 
                              num_in_page=graphene.Int(required=False))

    def resolve_all_room(root, info, **kwargs):
        page = kwargs.get("page", 1)
        num_in_page = kwargs.get("num_in_page", 16)

        query_set = ParentRoomModel.objects.all()

        request = info.context

        if (request.user.is_authenticated) and isTutor(request.user):
            tutor_not_known_room = (~Q(waitingtutormodel__tutor__user=request.user) & 
                                    ~Q(listinvitedmodel__tutor__user=request.user) &
                                    ~Q(tryteachingmodel__tutor__user=request.user) &
                                    ~Q(tutorteachingmodel__tutor__user=request.user)
                                    )
            query_set = query_set.filter(tutor_not_known_room)

        if (request.user.is_authenticated) and isParent(request.user):
            parent_not_create_room = (~Q(parent__user=request.user)
                                      )
            query_set = query_set.filter(parent_not_create_room)
        
        query_set = query_set.filter(tutorteachingmodel = None)
        query_set = query_set.order_by("-create_at")
        result = paginator_function(query_set, num_in_page, page)

        return {
            'result': result,
            'num_pages': result.paginator.num_pages
        }


    # lay room thong qua id
    room_by_id = graphene.Field(ParentRoomType, 
                                token=graphene.String(required=False),
                                id=graphene.ID(required=True))

    def resolve_room_by_id(root, info, **kwargs):
        id = kwargs.get('id')
        return ParentRoomModel.objects.get(pk=id)


    # lay danh sach cac tutor
    all_tutor = graphene.Field(ResultAllTutor, 
                               token=graphene.String(required=False),
                               page=graphene.Int(required=False), 
                               num_in_page=graphene.Int(required=False))

    def resolve_all_tutor(root, info, **kwargs):
        page = kwargs.get("page", 1)
        num_in_page = kwargs.get("num_in_page", 16)

        result = paginator_function(TutorModel.objects.all(), num_in_page, page)

        return {
            'result': result,
            'num_pages': result.paginator.num_pages
        }

    # lay waiting_item bang id
    waiting_by_id = graphene.Field(WaitingTutorType,
                                   id=graphene.ID(required=True))

    def resolve_waiting_by_id(root, info, **kwargs):
        id = kwargs.get("id")
        return WaitingTutorModel.objects.get(pk=id)

    # lay tutor teaching bang id
    tutor_teaching_by_id = graphene.Field(TutorTeachingType,
                                          id=graphene.ID(required=True))

    def resolve_tutor_teaching_by_id(root, info, **kwargs):
        id = kwargs.get("id")
        return TutorTeachingModel.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_parent_room = CreateParentRoomMutation.Field()

    create_waiting_tutor = CreateWaitingTutorMutation.Field()

    create_list_invited = CreateListInvitedMutation.Field()
    
    create_tutor_teaching = CreateTutorTeachingMutation.Field()

    # create_try_teaching = CreateTryTeachingMutation.Field()
    # update_try_teaching = UpdateTryTeachingMutation.Field()



