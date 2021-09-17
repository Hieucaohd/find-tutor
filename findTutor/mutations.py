import graphene

from findTutor.inputs import *
from findTutor.types import *
from findTutor.models import *

from findTutor.validateInputs import *
from findTutor.checkTutorAndParent import isTutor, isParent


class CreateParentRoomMutation(graphene.Mutation):
    class Arguments:
        input_fields = ParentRoomInput(required=True)


    parent_room = graphene.Field(ParentRoomType)

    @classmethod
    def mutate(cls, root, info, input_fields):
        parent = ParentModel.objects.get(user=info.context.user)
        parent_room = ParentRoomModel.objects.create(province_code   = input_fields.province_code, 
                                                     district_code   = input_fields.district_code,
                                                     ward_code       = input_fields.ward_code,
                                                     detail_location = input_fields.detail_location,
                                                     subject         = input_fields.subject,
                                                     lop             = input_fields.lop, 
                                                     day_can_teach   = input_fields.day_can_teach,
                                                     other_require   = input_fields.other_require,
                                                     parent          = parent)
        if input_fields.prices:
            for price in input_fields.prices:
                PriceModel.objects.create(parent_room     = parent_room,
                                          time_in_one_day = price.time_in_one_day,
                                          money_per_day   = price.money_per_day,
                                          type_teacher    = price.type_teacher,
                                          sex_of_teacher  = price.sex_of_teacher)
        return CreateParentRoomMutation(parent_room=parent_room)


class CreateListInvitedMutation(graphene.Mutation):
    class Arguments:
        input_fields = ListInvitedInput(required=True)

    list_invited = graphene.Field(ListInvitedType)

    @classmethod
    def mutate(cls, root, info, input_fields):

        attr = ValidateForListInvitedInput(input_fields=input_fields, info=info).validate()
        invited = ListInvitedModel.objects.create(**attr)
        return CreateListInvitedMutation(list_invited=invited)


class CreateTryTeachingMutation(graphene.Mutation):
    class Arguments:
        input_fields = TryTeachingInput(required=True)

    try_teaching = graphene.Field(TryTeachingType)

    @classmethod
    def mutate(cls, root, info, input_fields):
        attr = ValidateForTryTeachingInput(input_fields=input_fields, info=info).validate()
        try_teaching = TryTeachingModel.objects.create(**attr)
        return CreateTryTeachingMutation(try_teaching=try_teaching)
