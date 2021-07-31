from rest_framework import serializers

from rest_framework.exceptions import AuthenticationFailed

from . import google
from . import facebook

from .register import register_social_user


GOOGLE_CLIENT_ID = '149356398309-al2h86fudalenjccqquho57jkv5033pq.apps.googleusercontent.com'


class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError("token khong hop le hoac da het han. Vui long dang nhap lai.")

        # if user_data['aud'] != GOOGLE_CLIENT_ID:
        #     raise AuthenticationFailed("Ban dang co hack vao trang web cua chung toi.")

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(user_id, email, name, provider)


class FacebookAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'

            return register_social_user(user_id, email, name, provider)
        except:
            raise serializers.ValidationError("token khong hop le hoac da het han. Voi long dang nhap lai.")
