import graphene
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required

from .models import *
from authentication.models import User

class UserType(DjangoObjectType):
	class Meta:
		model = User

		# đây là thông tin có thể public của user 
		fields = (
				  #"id",
				  "username",
				  "email"
				  )

class TutorType(DjangoObjectType):
	class Meta:
		model = TutorModel

		# đây là các thông tin có thể public của gia sư
		fields = (
				  # thông tin của gia sư
				  #"id", 
				  "first_name", 
				  "last_name", 
				  "birthday",

				  # thông tin về địa chỉ cũng có thể là nhạy cảm 
				  "province_code", 
				  "district_code", 
				  "ward_code",

				  "profession",
				  "university",
				  "experience",
				  "achievement",
				  "lop_day",
				  )


class ParentType(DjangoObjectType):
	class Meta:
		model = ParentModel

		# đây là các thông tin có thể public của phụ huynh
		fields = (
				  # thông tin của phụ huynh
				  #"id",
				  "first_name",
				  "last_name",
				  "birthday",

				  # thông tin về địa chỉ cũng có thể là nhạy cảm
				  "province_code",
				  "district_code",
				  "ward_code",

				  # những lớp học mà phụ huynh tạo 
				  "parentroommodel_set",
				  )

	def resolve_first_name(self, info):
		request = info.context

		if request.user.is_authenticated:
			return self.first_name
		else:
			return None


class ParentRoomType(DjangoObjectType):
	class Meta:
		model = ParentRoomModel

		# đây là các thông tin có thể public của lớp học
		fields = (
				  # thông tin của lớp học
				  #"id",

				  # thông tin về địa chỉ cũng có thể là nhạy cảm
				  "province_code",
				  "district_code",
				  "ward_code",

				  "detail_location",
				  "subject",
				  "lop",
				  "isTeaching",
				  "create_at",
				  "day_can_teach",
				  "other_require",

				  # phụ huynh tạo ra lớp học
				  "parent"
				  )

	def resolve_parent(self, info):
		request = info.context

		if request.user.is_authenticated:
			return self.parent
		else:
			return None


class PriceType(DjangoObjectType):
	class Meta:
		model = PriceModel

class OldLocationType(DjangoObjectType):
	class Meta:
		model = OldLocationModel

class WaitingTutorType(DjangoObjectType):
	class Meta:
		model = WaitingTutorModel

class ListInvitedType(DjangoObjectType):
	class Meta:
		model = ListInvitedModel

class TryTeachingType(DjangoObjectType):
	class Meta:
		model = TryTeachingModel

class TutorTeachingType(DjangoObjectType):
	class Meta:
		model = TutorTeachingModel


def who_is(request):
	print("\nrequest")
	print(request)

	print("\ndir request")
	print(dir(request))

	print("\nuser")
	print(request.user)

	print("\ndir user")
	print(dir(request.user))

	try:
		print(request.user.password)
	except:
		print("khong co mat khau")


class Query(graphene.ObjectType):
	# lấy thông tin của phụ huynh theo id  
	parent_by_id = graphene.Field(ParentType, id=graphene.Int())

	def resolve_parent_by_id(root, info, **kwargs):
		return ParentModel.objects.get(pk=id)

	# lấy thông tin của gia sư theo id
	tutor_by_id = graphene.Field(TutorType, id=graphene.Int(), token=graphene.String(required=False))

	def resolve_tutor_by_id(root, info, **kwargs):
		id = kwargs.get("id");

		# for debug
		request = info.context
		who_is(request)

		return TutorModel.objects.get(pk=id)

	# lấy tất cả các lớp học
	all_room = graphene.List(ParentRoomType)

	def resolve_all_room(root, info, **kwargs):
		# for debug
		request = info.context
		who_is(request)

		return ParentRoomModel.objects.all()

schema = graphene.Schema(query=Query)
