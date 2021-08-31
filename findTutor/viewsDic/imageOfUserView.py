from rest_framework.response import Response
from rest_framework import status

from .baseView import CreateBaseView, UpdateBaseView, DeleteBaseView

from ..models import ImageOfUserModel
from ..serializers import ImageOfUserSerializer

from ..permissions import is_owner

from django.conf import settings
from ..firebaseConfig import storage, get_url


class ImageOfUserList(CreateBaseView):
	modelBase = ImageOfUserModel
	serializerBase = ImageOfUserSerializer

	def post(self, request, format=None):
		serializer = self.serializerBase(data=request.data)
		if serializer.is_valid():

			if settings.USE_FIREBASE:
				image = request.data.get("image")

				image_url = None
				if image:
					image_url = get_url(image, "user_image")

				serializer.save(user=request.user, image=image_url)

			else:
				serializer.save(user=request.user)

			return Response(serializer.data)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class ImageOfUserDetail(UpdateBaseView, DeleteBaseView):
	modelBase = ImageOfUserModel
	serializerBase = ImageOfUserSerializer

	def put(self, request, pk, format=None):
		get_image = self.get_object(pk)

		if not is_owner(request, get_image.user):
			return Response(status=status.HTTP_403_FORBIDDEN)

		serializer = self.serializerBase(get_image, data=request.data)
		image = request.data.get("image")

		if serializer.is_valid():

			if image:
				old_image = ImageOfUserModel()
				old_image.image = get_image.image
				old_image.user = get_image.user
				old_image.type_image = get_image.type_image  
				old_image.is_public = False
				old_image.is_using = False
				old_image.save()

			if settings.USE_FIREBASE and image:
				image_url = get_url(image, "user_image")
				serializer.save(image=image_url)
			else:
				serializer.save()
			return Response(serializer.data)
		return Response(status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		get_image = self.get_object(pk)

		if not is_owner(request, get_image.user):
			return Response(status=status.HTTP_403_FORBIDDEN)

		return super().delete(request, pk)








