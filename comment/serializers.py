from rest_framework import serializers
from .models import *


class CommentAboutUserSerializer(serializers.ModelSerializer):
	about_who = serializers.PrimaryKeyRelatedField(read_only=True, source='about_who.id')
	user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
	belong_to = serializers.PrimaryKeyRelatedField(read_only=True, source='belong_to.id')

	class Meta:
		model = CommentAboutUserModel
		fields = '__all__'


class CommentAboutParentRoomSerializer(serializers.ModelSerializer):
	about_who = serializers.PrimaryKeyRelatedField(read_only=True, source='about_who.id')
	user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
	belong_to = serializers.PrimaryKeyRelatedField(read_only=True, source='belong_to.id')

	class Meta:
		model = CommentAboutParentRoomModel
		fields = '__all__'
