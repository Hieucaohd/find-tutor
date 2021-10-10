from django.shortcuts import render

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (RegisterSerializer, 
                          LoginSerializer, 
                          LogoutSerializer, 
                          GetInforByTokenSerializer,
                          ChangePasswordSerializer,
                          LinkSerializer)
from .models import User, LinkModel
from .utils import Util

from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse

from django.conf import settings

import jwt

from findTutor.models import TutorModel, ParentModel
from findTutor.viewsDic.baseView import UpdateBaseView, DeleteBaseView

from .showInforAboutAnUser import inforAboutUser

from authentication.models import LinkModel

import copy

import threading


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def send_verify_email(self, request, user):
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('verify-email')
        absurl = 'https://' + current_site + relative_link + "?token=" + str(token)

        email_body = "Xin chào " + user.username + ". Cảm ơn bạn đã đăng kí tài khoản tại findTutor. Hãy nhấp vào link dưới đây để xác thực tài khoản của bạn nhé \n" + absurl
        data = {
            'email_body': email_body,
            'email_subject': "Tìm gia sư",
            'to_email': [user.email],
        }

        Util.send_email(data)
        

    def post(self, request, format=None):
        user_data_from_request = request.data
        serializer = self.serializer_class(data=user_data_from_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # send email to user
        user = User.objects.get(email=user_data['email'])

        threading.Thread(target=self.send_verify_email, kwargs={"request": request,
                                                                "user": user}).start()

        return Response(inforAboutUser(user))


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': "Successfully verified"}, status=status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = User.objects.get(email=data.get('email'))

        return Response(inforAboutUser(user), status=status.HTTP_200_OK)

class ChangePassword(APIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, format=None):
        request.data['email'] = request.user.email
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = User.objects.get(email=data.get('email'))

        return Response(inforAboutUser(user), status=status.HTTP_200_OK)


class Logout(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GetInforByToken(generics.GenericAPIView):
    serializer_class = GetInforByTokenSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return Response(inforAboutUser(request.user))


class LinkDetail(UpdateBaseView, DeleteBaseView):
    modelBase = LinkModel
    serializerBase = LinkSerializer

    def put(self, request, pk, format=None):
        link_item = self.get_object(pk)
        if not request.user == link_item.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().put(request, pk, format)

    def delete(self, request, pk, format=None):
        link_item = self.get_object(pk)
        if not link_item.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().put(request, pk, format)


