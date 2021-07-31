# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
#
# from ..models import TutorModel, ParentModel
#
#
# class CustomAuthToken(ObtainAuthToken):
#
#     def isTutor(self, user):
#         take_tutor_request = TutorModel.objects.filter(user=user)
#         if take_tutor_request:
#             return True
#         return False
#
#     def isParent(self, user):
#         take_parent_request = ParentModel.objects.filter(user=user)
#         if take_parent_request:
#             return True
#         return False
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token = Token.objects.get(user=user)
#
#         type_tutor = self.isTutor(user)
#         type_parent = self.isParent(user)
#
#         return Response({
#             'token': token.key,
#             'id': user.pk,
#             'type_tutor': type_tutor,
#             'type_parent': type_parent,
#         })