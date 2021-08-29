from rest_framework.response import Response
from rest_framework import status

from .baseView import CreateBaseView, UpdateBaseView, DeleteBaseView

from ..models import ImagePrivateUserModel, OldImagePrivateUserModel
from ..serializers import ImagePrivateUserSerializer

from ..permissions import is_owner


class ImagePrivateUserList(CreateBaseView):
	modelBase = ImagePrivateUserModel
	serializerBase = ImagePrivateUserSerializer

	def post(self, request, format=None):
		serializer = self.serializerBase(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)
			return Response(serializer.data)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class ImagePrivateUserDetail(UpdateBaseView, DeleteBaseView):
	modelBase = ImagePrivateUserModel
	serializerBase = ImagePrivateUserSerializer

	# def which_field_updated(self, request):


	def put(self, request, format=None):
		get_private_image = self.modelBase.objects.get(user=request.user)

		serializer = self.serializerBase(get_private_image, data=request.data)

		avatar = request.data.get('avatar')
		identity_card = request.data.get('identity_card')
		student_card = request.data.get('student_card')


		print(avatar)
		print(identity_card)
		print(student_card)

		if serializer.is_valid():
			array_item = []
			
			if avatar and get_private_image.avatar:
				old_avatar = OldImagePrivateUserModel()
				old_avatar.image = get_private_image.avatar
				old_avatar.type_image = OldImagePrivateUserModel.type_image_array[0]	# avatar
				array_item.append(old_avatar)

			if identity_card and get_private_image.identity_card:
				old_identity_card = OldImagePrivateUserModel()
				old_identity_card.image = get_private_image.identity_card
				old_identity_card.type_image = OldImagePrivateUserModel.type_image_array[1]	# identity_card
				array_item.append(old_identity_card)

			if student_card and get_private_image.student_card:
				old_student_card = OldImagePrivateUserModel()
				old_student_card.image = get_private_image.student_card
				old_student_card.type_image = OldImagePrivateUserModel.type_image_array[2]	# student_card
				array_item.append(student_card)

			for item in array_item:
				item.type_action = OldImagePrivateUserModel.type_action_array[0]
				item.user = request.user
				item.save()

			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

	def delete(self, request, format=None):
		get_private_image = self.modelBase.objects.get(user=request.user)
		id_of_item = get_private_image.id
		get_private_image.delete()
		return Response(
				{
					"id": id_of_item
				}
			)

