from rest_framework.response import Response
from rest_framework import status, permissions

from django.http import Http404

from ..models import ParentRoomModel, ParentModel
from ..serializers import ParentRoomSerializer

from .baseView import *
from .permisstions import IsParent, IsOwnerOfRoom


class PermissionParentRoom(TakeObjectView):

    def isParent(self, request):
        parent_request = ParentModel.objects.filter(user=request.user)
        if parent_request:
            return True
        return False

    def isParentOwner(self, request, pk):
        obj = self.get_object(pk)  # room: obj.parent -> parent
        return obj.parent.user == request.user


class ParentRoomList(ListCreateBaseView, PermissionParentRoom):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = ParentRoomModel
    serializerBase = ParentRoomSerializer

    def get(self, request, format=None):
        # all is a query params.
        # If all = 0: just take the room of request.user.parent.
        # else all != 0 or all does not exit: take all the room in the database.

        all_number = int(request.query_params.get('all', 1))
        if all_number == 0:
            try:
                parent = ParentModel.objects.get(user=request.user)
            except ParentModel.DoesNotExist as e:
                raise Http404

            rooms = self.modelBase.objects.filter(parent=parent)
            serializer = self.serializerBase(rooms, many=True)
            return Response(serializer.data)
        else:
            return super().get(request)

    def post(self, request, format=None):
        if self.isParent(request):
            serializer = self.serializerBase(data=request.data)
            if serializer.is_valid():
                parent = ParentModel.objects.get(user=request.user)
                serializer.save(parent=parent)
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ParentRoomDetail(RetrieveUpdateDeleteBaseView, PermissionParentRoom):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = ParentRoomModel
    serializerBase = ParentRoomSerializer

    def put(self, request, pk, format=None):
        if self.isParent(request) and self.isParentOwner(request, pk):
            return super().put(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        if self.isParent(request) and self.isParentOwner(request, pk):
            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


