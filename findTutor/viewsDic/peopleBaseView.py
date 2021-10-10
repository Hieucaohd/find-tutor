from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from ..models import TutorModel
from ..serializers import TutorSerializer

from .baseView import *
from .permisstions import IsOwner

from authentication.models import LinkModel, User

import threading


class PeopleList(ListCreateBaseView):
    permission_classes = [permissions.IsAuthenticated]

    def save_link(self, links, user):
        for link in links:
            link['user'] = user
            LinkModel.objects.create(**link)

    def post(self, request, format=None):
        links = request.data.get("link", [])
        threading.Thread(target=self.save_link, kwargs={"links": links,
                                                        "user": request.user}).start()

        del request.data['link']
        serializer = self.serializerBase(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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

    def put(self, request, pk_user, format=None):
        user = User.objects.get(pk=pk_user)

        pk = None
        if hasattr(user, 'tutormodel'):
            pk = user.tutormodel.id
        elif hasattr(user, 'parentmodel'):
            pk = user.parentmodel.id
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if self.isOwner(request, pk):
            return super().put(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
