from ..models import ListInvitedModel, TutorModel, TryTeachingModel, ParentRoomModel
from ..serializers import ListInvitedSerializer, TryTeachingSerializer

from .baseView import ListCreateBaseView, RetrieveUpdateDeleteBaseView

from rest_framework import permissions, status
from rest_framework.response import Response

from findTutor.signals import tutor_out_room_signal
from findTutor.messages import RoomNotificationMessage

from django.http import Http404

import threading


class ListInvitedList(ListCreateBaseView):
    """
        Just tutor can see the list of Invited him/her.
    """
    permission_classes = [permissions.IsAuthenticated]

    modelBase = ListInvitedModel
    serializerBase = ListInvitedSerializer

    def get_pk_room(self, request):
        try:
            return int(request.query_params['pk_room'])
        except Exception as e:
            return False

    def get_room(self, request):
        pk_room = self.get_pk_room(request)
        try:
            return ParentRoomModel.objects.get(pk=pk_room)
        except ParentRoomModel.DoesNotExist as e:
            raise Http404

    def get_tutor_from_request(self, request):
        try:
            return TutorModel.objects.get(user=request.user)
        except TutorModel.DoesNotExist as e:
            raise Http404

    def get_for_tutor(self, request, format=None):
        """
            Return invited room for tutor from request when login.
        """
        tutor = self.get_tutor_from_request(request)
        list_invited = self.modelBase.objects.filter(tutor=tutor)
        serializer = self.serializerBase(list_invited, many=True)
        return Response(serializer.data)

    def get_for_room(self, request, format=None):
        """
            Return invited tutor for a room.
        """
        parent_room = self.get_room(request)
        list_invited = self.modelBase.objects.filter(parent_room=parent_room)
        serializer = self.serializerBase(list_invited, many=True)
        return Response(serializer.data)

    def get(self, request, format=None):
        if self.get_pk_room(request):
            return self.get_for_room(request)
        else:
            return self.get_for_tutor(request)

    def post(self, request, format=None):
        return Response(status=status.HTTP_403_FORBIDDEN)


class ListInvitedDetail(RetrieveUpdateDeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = ListInvitedModel
    serializerBase = ListInvitedSerializer

    def get_tutor_from_request(self, request):
        try:
            return TutorModel.objects.get(user=request.user)
        except TutorModel.DoesNotExist as e:
            raise Http404

    def isTutorBeInvited(self, request, pk):
        invite = self.get_object(pk)
        tutor = self.get_tutor_from_request(request)
        return invite.tutor == tutor

    def isRoomHasTutorTryTeaching(self, request, pk):
        parent_room = self.get_object(pk).parent_room
        try_teaching = TryTeachingModel.objects.filter(parent_room=parent_room)
        if try_teaching:
            return True
        return False

    def isParentInvited(self, request, pk):
        item = self.get_object(pk)
        return item.parent_room.parent.user == request.user

    def put(self, request, pk, format=None):
        """
            This is called when tutor agree to try teaching.
        """
        pass

    def delete(self, request, pk, format=None):
        """
            This is called when tutor not agree to try teaching or parent don't want tutor in list_invited any more.
        """
        invited_item = self.get_object(pk)

        kwargs = {
            "user_send": request.user,
            "instance": invited_item,
            "sender": self.__class__,
        }
        if self.isTutorBeInvited(request, pk):
            # notify for parent that tutor don't agree to try teaching.
            kwargs['user_receive'] = invited_item.parent_room.parent.user,
            kwargs['text'] = RoomNotificationMessage.generate_text(
                                id=RoomNotificationMessage.message_type['tutor_not_agree_parent_invite']['notify_parent'],
                                user_send=request.user
                            )
            threading.Thread(target=tutor_out_room_signal.send, kwargs=kwargs).start()

            return super().delete(request, pk)
        elif self.isParentInvited(request, pk):
            # notify for tutor that parent don't want him/her to try teaching any more.
            kwargs['user_receive'] = invited_item.tutor.user,
            kwargs['text'] = RoomNotificationMessage.generate_text(
                                id=RoomNotificationMessage.message_type['parent_cancel_invite_to_tutor']['notify_tutor'],
                                user_send=request.user
                            )
            threading.Thread(target=tutor_out_room_signal.send, kwargs=kwargs).start()

            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
