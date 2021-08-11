from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from ..models import TutorModel
from ..serializers import TutorSerializer

from .baseView import *
from .permisstions import IsOwner


class PeopleList(ListCreateBaseView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializerBase(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors)


class PeopleRetrieveView(RetrieveBaseView):
    permission_classes = [permissions.IsAuthenticated]


class PeopleUpdateView(UpdateBaseView):
    permission_classes = [permissions.IsAuthenticated & IsOwner]


class PeopleDetail(RetrieveBaseView, UpdateBaseView):
    # permission_classes = [permissions.IsAuthenticated]

    def isOwner(self, request, pk):
        obj = self.get_object(pk)
        return obj.user == request.user

    def put(self, request, pk, format=None):
        if self.isOwner(request, pk):
            return super().put(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
