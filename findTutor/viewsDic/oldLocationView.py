from ..serializers import OldLocationSerializer
from ..models import OldLocationModel

from rest_framework.response import Response
from rest_framework import status

from .baseView import ListCreateBaseView, RetrieveUpdateDeleteBaseView

from rest_framework.permissions import IsAuthenticated


class OldLocationList(ListCreateBaseView):
    permission_classes = [IsAuthenticated]
    serializerBase = OldLocationSerializer
    modelBase = OldLocationModel

    def get(self, request, format=None):
        old_location_list = self.modelBase.objects.filter(user=request.user)
        serializer = self.serializerBase(old_location_list, many=True)
        data = serializer.data
        return Response(data)


class OldLocationDetail(RetrieveUpdateDeleteBaseView):
    authentication_classes = [IsAuthenticated]
    serializerBase = OldLocationSerializer
    modelBase = OldLocationModel

    def isOwner(self, request, pk):
        return self.get_object(pk).user == request.user

    def put(self, request, pk, format=None):
        if self.isOwner(request, pk):
            return super().put(request, pk)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if self.isOwner(request, pk):
            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
