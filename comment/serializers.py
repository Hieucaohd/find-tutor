from rest_framework import serializers
from .models import *


class CommentBaseSerializer():
	about_who = serializers.PrimaryKeyRelatedField(read_only=True, source='about_who.id')
	user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')


class CommentAboutTutorSerializer(CommentBaseSerializer, serializers.ModelSerializer):
	class Meta:
		model = CommentAboutTutorModel
		fields = '__all__'


class CommentAboutParentSerializer(CommentBaseSerializer, serializers.ModelSerializer):
	class Meta:
		model = CommentAboutParentModel
		fields = '__all__'


class CommentAboutParentRoomSerializer(CommentBaseSerializer, serializers.ModelSerializer):
	class Meta:
		model = CommentAboutParentRoomModel
		fields = '__all__'
