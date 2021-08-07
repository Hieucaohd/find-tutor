from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import CommentAboutTutorModel, CommentAboutParentModel, CommentAboutParentRoomModel
from .serializers import CommentAboutTutorSerializer, CommentAboutParentSerializer, CommentAboutParentRoomSerializer

from findTutor.viewsDic.baseView import UpdateBaseView, DeleteBaseView


class CommentListBaseView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	modelBase = None
	serializerBase = None

	def post(self, request, format=None):
		about_who_pk = request.query_params.get('about_who_id', 0)

		if about_who_pk:
			about_who = self.modelBase.get(pk=about_who_pk)
			serializer = self.serializerBase(data=request.data)
			if serializer.is_valid():
				serializer.save(about_who=about_who, user=request.user)

				data = serializer.data

				return Response(data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentAboutTutorList(CommentListBaseView):
	modelBase = CommentAboutTutorModel
	serializerBase = CommentAboutTutorSerializer


class CommentAboutParentList(CommentListBaseView):
	modelBase = CommentAboutParentModel
	serializerBase = CommentAboutParentSerializer


class CommentAboutParentRoomList(CommentListBaseView):
	modelBase = CommentAboutParentRoomModel
	serializerBase = CommentAboutParentRoomSerializer


class CommentDetailBaseView(UpdateBaseView, DeleteBaseView):
	def isOwner(self, request, pk):
		return self.get_object(pk).user == request.user

	def put(self, request, pk, format=None):
		if self.isOwner(request, pk):
			return super().put(request, pk)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def delete(self, request, pk):
		if self.isOwner(request, pk):
			return super().delete(request, pk)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)


class CommentAboutTutorDetail(CommentDetailBaseView):
	modelBase = CommentAboutTutorModel
	serializerBase = CommentAboutTutorSerializer


class CommentAboutParentDetail(CommentDetailBaseView):
	modelBase = CommentAboutParentModel
	serializerBase = CommentAboutParentSerializer


class CommentAboutParentRoomDetail(CommentDetailBaseView):
	modelBase = CommentAboutParentRoomModel
	serializerBase = CommentAboutParentRoomSerializer


























