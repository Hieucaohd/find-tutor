from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import GoogleAuthSerializer, FacebookAuthSerializer

# Create your views here.


class GoogleAuth(generics.GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        data = (validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookAuth(generics.GenericAPIView):
    serializer_class = FacebookAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        data = (validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
