from .baseView import *

from ..models import TryTeachingModel, TutorModel, ParentRoomModel, TutorTeachingModel, ListInvitedModel, WaitingTutorModel
from ..serializers import TryTeachingSerializer, TutorTeachingSerializer

from rest_framework.response import Response
from rest_framework import status, permissions


class TryTeachingList(ListBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = TryTeachingModel
    serializerBase = TryTeachingSerializer

    def get_for_tutor(self, request):
        tutor_request = TutorModel.objects.get(user=request.user)
        list_try_teaching = self.modelBase.objects.filter(tutor=tutor_request)
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
        return item.parent_room.parent.user == request.user

    def isTutorTryTeaching(self, request, pk):
        item = self.get_object(pk)
        return item.tutor.user == request.user

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = self.serializerBase(item, data=request.data)

        if self.isParentOwner(request, pk):
            if serializer.is_valid():
                serializer.save(parent_agree=True)
                data = serializer.data
                # websocket for tutor that parent agree for him/her teach.
            else:
                return Response(serializer.errors)
        elif self.isTutorTryTeaching(request, pk):
            if serializer.is_valid():
                serializer.save(tutor_agree=True)
                data = serializer.data
                # websocket for parent that tutor agree for teaching their children.
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if item.tutor_agree and item.parent_agree:
               
            new_teaching = TutorTeachingModel.objects.create(parent_room=item.parent_room, tutor=item.tutor)
            data = TutorTeachingSerializer(new_teaching).data;
            data["tutor_agree"] = True;
            data["parent_agree"] = True;
            # delete from try_teaching.
            item.delete()

            # Take list invited of room to waiting.
            list_invited_of_room = ListInvitedModel.objects.filter(parent_room=item.parent_room)
            for invited in list_invited_of_room:
                # websocket for each tutor in list_invited that the room has a tutor in teaching.

                WaitingTutorModel.objects.create(parent_room=item.parent_room, tutor=item.tutor)
            # Delete invited list.
            list_invited_of_room.delete()

        print(data)
        return Response(data)

    def delete(self, request, pk, format=None):
        if self.isParentOwner(request, pk):
            # websocket for tutor that parent don't want him/her to continue teach.

            return super().delete(request, pk)
        elif self.isTutorTryTeaching(request, pk):
            # websocket for parent that tutor don't want to continue teach.

            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)











