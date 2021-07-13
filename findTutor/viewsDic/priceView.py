from ..serializers import PriceSerializer
from ..models import PriceModel, ParentRoomModel

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.http import Http404

from .baseView import *


class PriceList(ListBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = PriceModel
    serializerBase = PriceSerializer

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

    def isOwnerOfRoom(self, request):
        room = self.get_room(request)
        return room.parent.user == request.user

    def get(self, request, format=None):
        try:
            room = self.get_room(request)
            prices_of_room = self.modelBase.objects.filter(class_id=room)
            serializer = PriceSerializer(prices_of_room, many=True)
            return Response(serializer.data)
        except Http404 as e:
            pass

        return super().get(request=request)

    def post(self, request, format=None):
        if self.isOwnerOfRoom(request):
            room = self.get_room(request)
            serializer = self.serializerBase(data=request.data)
            if serializer.is_valid():
                serializer.save(class_id=room)
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PriceDetail(RetrieveUpdateDeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = PriceModel
    serializerBase = PriceSerializer

    def isOwnerOfPrice(self, request, pk):
        price_obj = self.get_object(pk)
        return price_obj.class_id.parent.user == request.user

    def put(self, request, pk, format=None):
        if self.isOwnerOfPrice(request, pk):
            return super().put(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        if self.isOwnerOfPrice(request, pk):
            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
