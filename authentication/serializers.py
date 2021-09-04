from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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
        
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):

        self.refresh_token = attrs['refresh_token']

        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            self.fail("bad_token")


class GetInforByTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['token']

        return attrs

