from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User

from django.contrib import auth

from findTutor.models import TutorModel, ParentModel


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    # def isTutor(self, user):
    #     take_tutor_request = TutorModel.objects.filter(user=user)
    #     if take_tutor_request:
    #         return True
    #     return False
    #
    # def isParent(self, user):
    #     take_parent_request = ParentModel.objects.filter(user=user)
    #     if take_parent_request:
    #         return True
    #     return False

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filter_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filter_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed("Ban da dang nhap bang email " + email +
                                       " bang " + filter_user_by_email[0].auth_provider +
                                       ". Hay dang nhap bang " + filter_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed("Ten dang nhap hoac mat khau khong dung.")
        if not user.is_active:
            raise AuthenticationFailed("Tai khoan dang bi khoa, voi long lien he voi admin de moi lai")
        # if not user.is_verified:
        #     raise AuthenticationFailed("Email chua duoc xac nhan, voi long xac nhan email")

        # type_tutor = self.isTutor(user)
        # type_parent = self.isParent(user)
        # token = user.tokens()

        # return {
        #     'email': user.email,
        #     'username': user.username,
        #     'token': token.get('access', ''),
        #     'id': user.id,
        #     'type_tutor': type_tutor,
        #     'type_parent': type_parent,
        # }

        return attrs
    #
    # def create(self, validated_data):
    #     email = validated_data.get('email', '')
    #     return User.objects.get(email=email)

