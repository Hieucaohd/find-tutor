from .baseView import *

from ..models import TutorTeachingModel, ParentRoomModel, TutorModel
from ..serializers import TutorTeachingSerializer

from rest_framework.response import Response
from rest_framework import status, permissions


class TutorTeachingList(ListBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = TutorTeachingModel
    serializerBase = TutorTeachingSerializer

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
        list_teaching = self.modelBase.objects.filter(parent_room=room)
        serializer = self.serializerBase(list_teaching, many=True)
        return Response(serializer.data)

    def get_for_tutor(self, request):
        tutor_request = TutorModel.objects.get(user=request.user)
        list_teaching = self.modelBase.objects.filter(tutor=tutor_request)
        serializer = self.serializerBase(list_teaching, many=True)
        return Response(serializer.data)

    def get(self, request, format=None):
        if self.get_pk_room(request):
            return self.get_for_room(request)
        else:
            return self.get_for_tutor(request)


class TutorTeachingDetail(DeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = TutorTeachingModel
    serializerBase = TutorTeachingSerializer

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        
        if request.user == item.parent_room.parent.user:
            return super().delete(request, pk)
        elif request.user == item.tutor.user:
            return super().delete(request, pk)
        
        return Response(status=status.HTTP_403_FORBIDDEN)





