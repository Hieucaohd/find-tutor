import graphene

from findTutor.inputs import *
from findTutor.messages import RoomNotificationMessage
from findTutor.types import *
from findTutor.models import *

from findTutor.signals import (parent_create_room_signal,
                               create_tutor_teaching_signal,
                               )

from findTutor.validateInputs import *
from findTutor.checkTutorAndParent import isTutor, isParent

from threading import Thread
from multiprocessing import Process

from findTutor.checkTutorAndParent import isTutor, isParent

from django import db


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
        # signal
        db.connections.close_all()
        Process(target=parent_create_room_signal.send, kwargs={"sender": ParentRoomModel, 
                                                               "instance": parent_room, 
                                                               "info": info}).start()
        return CreateParentRoomMutation(parent_room=parent_room)


class CreateWaitingTutorMutation(graphene.Mutation):
    class Arguments:
        input_fields = WaitingTutorInput(required=True)

    waiting_tutor = graphene.Field(WaitingTutorType)

    @classmethod
    def mutate(cls, root, info, input_fields):
        attr = ValidateForWaitingTutorInput(input_fields=input_fields, info=info).validate()
        waiting_tutor = WaitingTutorModel.objects.create(**attr)

        return CreateWaitingTutorMutation(waiting_tutor=waiting_tutor)


class CreateListInvitedMutation(graphene.Mutation):
    class Arguments:
        input_fields = ListInvitedInput(required=True)

    list_invited = graphene.Field(ListInvitedType)

    @classmethod
    def mutate(cls, root, info, input_fields):

        attr = ValidateForListInvitedInput(input_fields=input_fields, info=info).validate()
        invited = ListInvitedModel.objects.create(**attr)
        return CreateListInvitedMutation(list_invited=invited)


class CreateTutorTeachingMutation(graphene.Mutation):
    class Arguments:
        input_fields = TutorTeachingInput(required=True)

    tutor_teaching = graphene.Field(TutorTeachingType)

    @classmethod
    def mutate(cls, root, info, input_fields):
        attr = ValidateForTutorTeachingInput(input_fields=input_fields, info=info).validate()
        tutor_teaching = TutorTeachingModel.objects.create(**attr)

        # signal
        user_send = info.context.user
        parent_room = tutor_teaching.parent_room
        kwargs = {
            "sender": ParentRoomModel,
            "user_send": user_send,
            "instance": tutor_teaching,
        }
        if isTutor(user_send):
            kwargs['user_receive'] = tutor_teaching.parent_room.parent.user
            kwargs['text'] = RoomNotificationMessage.generate_text(
                id=RoomNotificationMessage.message_type["tutor_agree_for_parent_to_teaching"]["notify_parent"],
                user_send=user_send
            )
            Thread(target=create_tutor_teaching_signal.send, kwargs=kwargs).start()
        elif isParent(user_send):
            kwargs['user_receive'] = tutor_teaching.tutor.user
            kwargs['text'] = RoomNotificationMessage.generate_text(
                id=RoomNotificationMessage.message_type["parent_agree_for_tutor_teaching"]["notify_tutor"],
                user_send=user_send
            )
            Thread(target=create_tutor_teaching_signal.send, kwargs=kwargs).start()

        return CreateTutorTeachingMutation(tutor_teaching=tutor_teaching)

"""
class CreateTryTeachingMutation(graphene.Mutation):
    class Arguments:
        input_fields = TryTeachingInput(required=True)

    try_teaching = graphene.Field(TryTeachingType)

    @classmethod
    def mutate(cls, root, info, input_fields):
        attr = ValidateForTryTeachingInput(input_fields=input_fields, info=info).validate()
        try_teaching = TryTeachingModel.objects.create(**attr)
        return CreateTryTeachingMutation(try_teaching=try_teaching)


class UpdateTryTeachingMutation(graphene.Mutation):
    class Arguments:
        input_fields = UpdateTryTeachingInput(required=True)

    try_teaching = graphene.Field(TryTeachingType)

    @classmethod
    def mutate(cls, root, info, input_fields):
        attr = ValidateForUpdateTryTeachingInput(input_fields=input_fields, info=info).validate()
        return UpdateTryTeachingMutation(try_teaching=attr)
"""



