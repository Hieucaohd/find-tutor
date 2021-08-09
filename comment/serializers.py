from rest_framework import serializers
from .models import *


# class CommentBaseSerializer():
# 	about_who = serializers.PrimaryKeyRelatedField(read_only=True, source='about_who.id')
# 	user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
# 	belong_to = serializers.PrimaryKeyRelatedField(read_only=True, source='belong_to.id')
# 	content = serializers.CharField()


class CommentAboutTutorSerializer(serializers.ModelSerializer):
	about_who = serializers.PrimaryKeyRelatedField(read_only=True, source='about_who.id')
	user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
	belong_to = serializers.PrimaryKeyRelatedField(read_only=True, source='belong_to.id')

	class Meta:
		model = CommentAboutTutorModel
		fields = '__all__'


class CommentAboutParentSerializer(serializers.ModelSerializer):
	about_who = serializers.PrimaryKeyRelatedField(read_only=True, source='about_who.id')
	user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
	belong_to = serializers.PrimaryKeyRelatedField(read_only=True, source='belong_to.id')

	class Meta:
		model = CommentAboutParentModel
		fields = '__all__'


class CommentAboutParentRoomSerializer(serializers.ModelSerializer):
	about_who = serializers.PrimaryKeyRelatedField(read_only=True, source='about_who.id')
	user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
	belong_to = serializers.PrimaryKeyRelatedField(read_only=True, source='belong_to.id')

	class Meta:
		model = CommentAboutParentRoomModel
		fields = '__all__'
