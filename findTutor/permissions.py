from findTutor.models import (TutorModel, 
                              ParentModel, 
                              ParentRoomModel, 
                              ListInvitedModel, 
                              WaitingTutorModel,
                              TryTeachingModel,
                              TutorTeachingModel)
from django.db.models import Q

def isParentOwnerOfRoom(id_user_of_parent, id_room):
    check = Q(parent__user__id=id_user_of_parent) & Q(pk=id_room)
    return ParentRoomModel.objects.filter(check).exists()


def isTutorInOneListOfRoom(model, id_user_of_tutor, id_room):
    check = Q(parent_room__id=id_room) & Q(tutor__user__id=id_user_of_tutor)
    return model.objects.filter(check).exists()

def isTutorInListInvitedOfRoom(id_user_of_tutor, id_room):
    return isTutorInOneListOfRoom(ListInvitedModel, id_user_of_tutor, id_room)

def isTutorInWaitingListOfRoom(id_user_of_tutor, id_room):
    return isTutorInOneListOfRoom(WaitingTutorModel, id_user_of_tutor, id_room)

def isTutorInTryTeachingOfRoom(id_user_of_tutor, id_room):
    return isTutorInOneListOfRoom(TryTeachingModel, id_user_of_tutor, id_room)

def isTutorInTutorTeachingOfRoom(id_user_of_tutor, id_room):
    return isTutorInOneListOfRoom(TutorTeachingModel, id_user_of_tutor, id_room)