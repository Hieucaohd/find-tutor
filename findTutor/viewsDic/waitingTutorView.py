from ..serializers import WaitingTutorSerializer
from ..models import TutorModel, ParentModel, WaitingTutorModel, ListInvitedModel, TutorTeachingModel

from rest_framework.response import Response
from rest_framework import status, permissions

from .relateParentRoomBaseView import ItemRelateListBaseView
from .baseView import RetrieveUpdateDeleteBaseView


class WaitingTutorList(ItemRelateListBaseView):
    modelBase = WaitingTutorModel
    serializerBase = WaitingTutorSerializer

    def isTutor(self, request):
        take_tutor_request = TutorModel.objects.filter(user=request.user)   # take_tutor_request is a list.
        if take_tutor_request:
            return True
        return False

    def hasTutorInListWaiting(self, request):
        take_tutor_request = TutorModel.objects.filter(user=request.user)   # take_tutor_request is a list.

        if take_tutor_request:
            tutor_request = take_tutor_request[0]
        else:
            return True

        room = self.get_room(request)
        list_waiting = self.modelBase.objects.filter(parent_room=room)
        for wait in list_waiting:
            if wait.tutor == tutor_request:
                return True
        return False

    def post(self, request, format=None):
        """
            Use when tutor want to join waiting list of a room parent.
        """
        if self.isTutor(request) and (not self.hasTutorInListWaiting(request)):
            room = self.get_room(request)
            tutor = TutorModel.objects.get(user=request.user)
            serializer = self.serializerBase(data=request.data)
            if serializer.is_valid():
                serializer.save(parent_room=room, tutor=tutor)
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class WaitingTutorDetail(RetrieveUpdateDeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = WaitingTutorModel
    serializerBase = WaitingTutorSerializer

    def isOwnerOfRoom(self, request, pk):
        waiting_obj = self.get_object(pk)
        return waiting_obj.parent_room.parent.user == request.user

    def isTutorCreate(self, request, pk):
        waiting_obj = self.get_object(pk)
        return waiting_obj.tutor.user == request.user

    def put(self, request, pk, format=None):
        """
            When parent (owner of room) invite tutor.
        """
        if self.isOwnerOfRoom(request, pk):
            waiting_obj = self.get_object(pk)
            serializer = self.serializerBase(waiting_obj, data=request.data)
            if serializer.is_valid():
                serializer.save(parent_invite=True)

                # take tutor to List Invited.
                ListInvitedModel.objects.create(parent_room=waiting_obj.parent_room, tutor=waiting_obj.tutor)

                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        """
            When parent or tutor don't want to continua waiting.
        """
        if self.isOwnerOfRoom(request, pk) or self.isTutorCreate(request, pk):
            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
