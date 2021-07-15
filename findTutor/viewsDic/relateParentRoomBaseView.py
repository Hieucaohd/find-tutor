from ..models import ParentRoomModel

from rest_framework.response import Response
from rest_framework import permissions, status

from django.http import Http404

from .baseView import *


class ItemRelateListBaseView(ListBaseView):
    permission_classes = [permissions.IsAuthenticated]

    def get_pk_room(self, request):
        try:
            return int(request.query_params['pk_room'])
        except Exception as e:
            raise Http404

    def get_room(self, request):
        pk_room = self.get_pk_room(request)
        try:
            return ParentRoomModel.objects.get(pk=pk_room)
        except ParentRoomModel.DoesNotExist as e:
            raise Http404

    def get(self, request, format=None):
        try:
            room = self.get_room(request)
            item_relate_to_room = self.modelBase.objects.filter(parent_room=room)
            serializer = self.serializerBase(item_relate_to_room, many=True)
            return Response(serializer.data)
        except Http404 as e:
            pass

        return super().get(request=request)
