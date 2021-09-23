from findTutor.checkTutorAndParent import isTutor, isParent
from findTutor.permissions import (isParentOwnerOfRoom, 
                                   isTutorInListInvitedOfRoom,
                                   isTutorInTryTeachingOfRoom,
                                   isTutorInTutorTeachingOfRoom)
from findTutor.models import *
from authentication.models import User

from findTutor.exceptions import *

def is_tutor_teaching_room(parent_room, tutor):
    try:
        if parent_room.tutorteachingmodel.tutor == tutor:
            return True
        else:
            return False
    except AttributeError:
        return False


class ValidateForListInvitedInput:
    def __init__(self, input_fields, info):
        self.user_of_parent = info.context.user
        self.id_parent_room = input_fields.id_parent_room
        self.id_user_of_tutor = input_fields.id_user_of_tutor

        if not info.context.user.is_authenticated:
            raise NeedAuthentication

    def validate_id_parent_room(self):
        return ParentRoomModel.objects.get(pk=self.id_parent_room)
        
    def validate_id_user_of_tutor(self):
        return TutorModel.objects.get(user__id=self.id_user_of_tutor)

    def is_parent_owner_room(self):
        parent_room = self.validate_id_parent_room()
        if parent_room.parent.user.id == self.user_of_parent.id:
            return parent_room
        else:
            raise ParentNotOwnerRoom

    

    def validate(self):
        parent_room = self.is_parent_owner_room()
        tutor = self.validate_id_user_of_tutor()

        if (parent_room.waitingtutormodel_set.filter(tutor=tutor).exists()):
            raise TutorWasInWaitingList

        elif (parent_room.listinvitedmodel_set.filter(tutor=tutor).exists()):
            raise TutorWasInListInvited

        # elif (parent_room.tryteachingmodel_set.filter(tutor=tutor).exists()):
        #     raise TutorWasInTryTeaching

        elif is_tutor_teaching_room(parent_room, tutor):
            raise TutorWasInTutorTeaching

        else:  
            return {
                "tutor": tutor,
                "parent_room": parent_room
            }

"""
class ValidateForTryTeachingInput:
    def __init__(self, input_fields, info):
        self.user = info.context.user
        self.input_fields = input_fields

        if not info.context.user.is_authenticated:
            raise NeedAuthentication

    def validate_for_parent(self):
        id_waiting_list = self.input_fields.id_waiting_list
        waiting_item = WaitingTutorModel.objects.get(pk=id_waiting_list)
        parent_room = waiting_item.parent_room
        tutor = waiting_item.tutor

        if not parent_room.parent.user == self.user:
            raise ParentNotOwnerRoom

        elif parent_room.tryteachingmodel_set.filter(tutor=tutor).exists():
            raise TutorWasInTryTeaching

        elif is_tutor_teaching_room(parent_room, tutor):
            raise TutorWasInTutorTeaching

        else:
            waiting_item.delete()
            return {
                "tutor": tutor,
                "parent_room": parent_room
            }

    def validate_for_tutor(self):
        id_list_invited = self.input_fields.id_list_invited
        invited_item = ListInvitedModel.objects.get(pk=id_list_invited)
        parent_room = invited_item.parent_room
        tutor = TutorModel.objects.get(user=self.user)

        if not invited_item.tutor == tutor:
            raise TutorNotInvited

        elif parent_room.tryteachingmodel_set.filter(tutor=tutor).exists():
            raise TutorWasInTryTeaching

        elif is_tutor_teaching_room(parent_room, tutor):
            raise TutorWasInTutorTeaching

        else:
            invited_item.delete()
            return {
                "tutor": tutor,
                "parent_room": parent_room
            }

    def validate(self):
        if isTutor(self.user):
            return self.validate_for_tutor()
        elif isParent(self.user):
            return self.validate_for_parent()


class ValidateForUpdateTryTeachingInput:
    def __init__(self, input_fields, info) -> None:
        self.user = info.context.user
        self.input_fields = input_fields

        if not info.context.user.is_authenticated:
            raise NeedAuthentication

    def validate(self):
        id_try_teaching = self.input_fields.id_try_teaching
        try_teaching = TryTeachingModel.objects.get(pk=id_try_teaching)
        parent_room = try_teaching.parent_room

        try:
            tutor_teaching = parent_room.tutorteachingmodel
            raise ParentRoomIsTeaching
        except AttributeError:
            if isTutor(self.user) and try_teaching.tutor.user == self.user:
                if hasattr(self.input_fields, "tutor_agree"):
                    try_teaching.tutor_agree = self.input_fields.tutor_agree
                    try_teaching.save()
                return try_teaching
            elif isParent(self.user) and try_teaching.parent_room.parent.user == self.user:
                if hasattr(self.input_fields, "parent_agree"):
                    try_teaching.parent_agree = self.input_fields.parent_agree
                    try_teaching.save()
                return try_teaching
            else:
                raise Exception("Ban khong the thuc hien hanh dong nay.")
"""

class ValidateForWaitingTutorInput:
    def __init__(self, input_fields, info):
        self.user = info.context.user
        self.input_fields = input_fields

        if not info.context.user.is_authenticated:
            raise NeedAuthentication

    def validate(self):
        id_parent_room = self.input_fields.id_parent_room
        parent_room = ParentRoomModel.objects.get(pk=id_parent_room)
        tutor = TutorModel.objects.get(user=self.user)
        
        if (parent_room.waitingtutormodel_set.filter(tutor=tutor).exists()):
            raise TutorWasInWaitingList

        elif (parent_room.listinvitedmodel_set.filter(tutor=tutor).exists()):
            raise TutorWasInListInvited
        
        # elif (parent_room.tryteachingmodel_set.filter(tutor=tutor).exists()):
        #     raise TutorWasInTryTeaching

        elif is_tutor_teaching_room(parent_room, tutor):
            raise TutorWasInTutorTeaching

        else:  
            return {
                "tutor": tutor,
                "parent_room": parent_room
            }


# class ValidateForTutorTeachingInput:
#     def __init__(self, input_fields, info) -> None:
#         self.user = info.context.user
#         self.input_fields = input_fields

#         if not info.context.user.is_authenticated:
#             raise NeedAuthentication

#     def validate(self):
#         id_try_teaching = self.input_fields.id_try_teaching
#         try_teaching = TryTeachingModel.objects.get(pk=id_try_teaching)
#         parent_room = try_teaching.parent_room

#         attr = {
#             "tutor": try_teaching.tutor,
#             "parent_room": try_teaching.parent_room
#         }

#         try:
#             tutor_teaching = parent_room.tutorteachingmodel
#             raise ParentRoomIsTeaching
#         except AttributeError:
#             if try_teaching.tutor_agree and try_teaching.parent_agree:
#                 if isTutor(self.user) and try_teaching.tutor.user == self.user:
#                     try_teaching.delete()
#                     return attr
#                 elif isParent(self.user) and try_teaching.parent_room.parent.user == self.user:
#                     try_teaching.delete()
#                     return attr
#                 else:
#                     raise Exception("Ban khong duoc phep thuc hien hanh dong nay.")
#             else:
#                 raise Exception("phu huynh hoac gia su chua dong y de day chinh thuc.")

class ValidateForTutorTeachingInput:
    def __init__(self, input_fields, info):
        self.user = info.context.user
        self.input_fields = input_fields

        if not info.context.user.is_authenticated:
            raise NeedAuthentication

    def validate_for_parent(self):
        id_waiting_list = self.input_fields.id_waiting_list
        waiting_item = WaitingTutorModel.objects.get(pk=id_waiting_list)
        parent_room = waiting_item.parent_room
        tutor = waiting_item.tutor

        if not parent_room.parent.user == self.user:
            raise ParentNotOwnerRoom

        elif hasattr(parent_room, "tutorteachingmodel"):
            raise ParentRoomIsTeaching

        else:
            waiting_item.delete()
            return {
                "tutor": tutor,
                "parent_room": parent_room
            }

    def validate_for_tutor(self):
        id_list_invited = self.input_fields.id_list_invited
        invited_item = ListInvitedModel.objects.get(pk=id_list_invited)
        parent_room = invited_item.parent_room
        tutor = TutorModel.objects.get(user=self.user)

        if not invited_item.tutor == tutor:
            raise TutorNotInvited

        elif hasattr(parent_room, "tutorteachingmodel"):
            raise ParentRoomIsTeaching

        else:
            invited_item.delete()
            return {
                "tutor": tutor,
                "parent_room": parent_room
            }

    def validate(self):
        if isTutor(self.user):
            return self.validate_for_tutor()
        elif isParent(self.user):
            return self.validate_for_parent()