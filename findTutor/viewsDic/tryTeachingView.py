from .baseView import *

from ..models import TryTeachingModel, TutorModel, ParentRoomModel, TutorTeachingModel, ListInvitedModel, WaitingTutorModel
from ..serializers import TryTeachingSerializer

from rest_framework.response import Response
from rest_framework import status, permissions


class TryTeachingList(ListBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = TryTeachingModel
    serializerBase = TryTeachingSerializer

    def get_for_tutor(self, request):
        tutor_request = TutorModel.objects.get(user=request.user)
        list_try_teaching = self.serializerBase.objects.filter(tutor=tutor_request)
        serializer = self.serializerBase(list_try_teaching, many=True)
        return Response(serializer.data)

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

    def get_for_room(self, request):
        room = self.get_room(request)
        list_try_teaching = self.modelBase.objects.filter(parent_room=room)
        serializer = self.serializerBase(list_try_teaching, many=True)
        return Response(serializer.data)

    def get(self, request, format=None):
        if self.get_pk_room(request):
            return self.get_for_room(request)
        else:
            return self.get_for_tutor(request)


class TryTeachingDetail(RetrieveUpdateDeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = TryTeachingModel
    serializerBase = TryTeachingSerializer

    def isParentOwner(self, request, pk):
        item = self.get_object(pk)
        return item.parent_room.paren.user == request.user

    def isTutorTryTeaching(self, request, pk):
        item = self.get_object(pk)
        return item.tutor.user == request.user

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = self.serializerBase(item, data=request.data)

        if self.isParentOwner(request, pk):
            if serializer.is_valid():
                serializer.save(parent_agree=True)
            else:
                return Response(serializer.errors)
        elif self.isTutorTryTeaching(request, pk):
            if serializer.is_valid():
                serializer.save(tutor_agree=True)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if item.tutor_agree and item.parent_agree:
            TutorTeachingModel.objects.create(parent_room=item.parent_room, tutor=item.tutor)

            # Delete tutor from waiting list.
            tutor_need_delete = WaitingTutorModel.objects.get(tutor=item.tutor)
            tutor_need_delete.delete()

            # Take list invited of room to waiting.
            # Delete invited list.
            ListInvitedModel.objects.filter(parent_room=item.parent_room).delete()
            # Set parent_invite in waiting list all to False.
            WaitingTutorModel.objects.filter(parent_invite=True).update(parent_invite=False)

        return Response(serializer.data)











