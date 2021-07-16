from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from ..models import TutorModel, ParentModel


class ModelAndSerializer:
    modelBase = None
    serializerBase = None


class ListBaseView(APIView, ModelAndSerializer):

    def get(self, request, format=None):
        items = self.modelBase.objects.all()
        serializer = self.serializerBase(items, many=True)
        return Response(serializer.data)


class CreateBaseView(APIView, ModelAndSerializer):

    def post(self, request, format=None):
        serializer = self.serializerBase(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ListCreateBaseView(ListBaseView, CreateBaseView):
    pass


class TakeObjectView(APIView, ModelAndSerializer):

    def get_object(self, pk):
        try:
            obj = self.modelBase.objects.get(pk=pk)
        except self.modelBase.DoesNotExist as e:
            raise Http404
        else:
            self.check_object_permissions(self.request, obj)
            return obj


class RetrieveBaseView(TakeObjectView):

    def get(self, request, pk, format=None):
        item = self.get_object(pk=pk)
        serializer = self.serializerBase(item, many=False)
        return Response(serializer.data)


class UpdateBaseView(TakeObjectView):

    def put(self, request, pk, format=None):
        item = self.get_object(pk=pk)
        serializer = self.serializerBase(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class DeleteBaseView(TakeObjectView):

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveUpdateDeleteBaseView(RetrieveBaseView, UpdateBaseView, DeleteBaseView):
    pass






