from authentication.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager

from findTutor.checkTutorAndParent import isTutor, isParent

from rest_framework.exceptions import AuthenticationFailed


def register_social_user(user_id, email, name, provider):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email:

        if provider == filtered_user_by_email[0].auth_provider:

            register_user = authenticate(email=email, password=filtered_user_by_email[0].password)

            user = filtered_user_by_email[0]
            type_tutor = isTutor(user)
            type_parent = isParent(user)
            token = user.tokens()

            return {
                'email': user.email,
                'username': user.username,
                'token': token.get('access', ''),
                'refresh_token': token.get('refresh', ''),
                'id': user.id,
                'type_tutor': type_tutor,
                'type_parent': type_parent,
            }

        else:
            raise AuthenticationFailed("Ban da su dung email " + email + " de dang nhap bang " +
                                       filtered_user_by_email[0].auth_provider +
                                       ". Hay su dung " + filtered_user_by_email[0].auth_provider +
                                       " de dang nhap.")
    else:
        password = make_password(BaseUserManager().make_random_password())
        user = User.objects.create_user(username=name, password=password, email=email)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=password)
        token = new_user.tokens()
        return {
            'email': new_user.email,
            'username': new_user.username,
            'token': token.get('access', ''),
            'refresh_token': token.get('refresh', ''),
            'id': new_user.id,
            'type_tutor': False,
            'type_parent': False,
        }