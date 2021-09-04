import graphene
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required

from .models import *
from authentication.models import User

#from comment.schema import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q


def paginator_function(query_set, num_in_page, page):
	paginator = Paginator(query_set, num_in_page)

	try:
		list_item = paginator.page(page)
	except PageNotAnInteger:
		print("not integer")
		list_item = paginator.page(1)
	except EmptyPage:
		print("empty page")
		list_item = paginator.page(paginator.num_pages)

	return list_item


def is_owner(people, info):
	if info.context.user == people.user:
		return True
	return False


class UserType(DjangoObjectType):
	class Meta:
		model = User
		fields = (
				  "id",
				  "username",
				  "tutormodel",
				  "parentmodel",
				  "imageprivateusermodel",
				  "oldimageprivateusermodel_set",
				  "imageofusermodel_set",

				  # # comment ve user
				  # "commentaboutusermodel_set",
				  )


class TutorType(DjangoObjectType):
	class Meta:
		model = TutorModel
		fields =  (
				  "first_name", 
				  "last_name",
				  "birthday",

				  "province_code", 
				  "district_code", 
				  "ward_code",

				  # đia chỉ chi tiết cũng nhạy cảm
				  "detail_location",

				  "profession",
				  "university",
				  "experience",
				  "achievement",
				  "lop_day",
				  "khu_vuc_day",

				  # thông tin cực kì nhạy cảm
				  "number_phone",
				  "number_of_identity_card",

				  # thong tin ve lop
				  'waitingtutormodel_set',
				  'listinvitedmodel_set',
				  'tryteachingmodel_set',
				  'tutorteachingmodel_set',
				  )


	# self là một đối tượng của TutorModel, không phải là đối tượng của TutorType

	def resolve_detail_location(self, info):
		if is_owner(self, info):
			return self.detail_location
	
	def resolve_number_phone(self, info):
		if is_owner(self, info):
			return self.number_phone

	def resolve_number_of_identity_card(self, info):
		if is_owner(self, info):
			return self.number_of_identity_card


class OldImagePrivateUserType(DjangoObjectType):
	class Meta:
		model = OldImagePrivateUserModel
		fields = (
				 "image",
				 "type_image",
				 "type_action",
				 "create_at",
				 )

	def resolve_image(self, info):
		if is_owner(self, info):
		 	return self.image
		elif self.type_image == OldImagePrivateUserModel.type_image_array[0]:
			return self.image
		else:
			return ''

	@classmethod
	def get_queryset(cls, queryset, info):
		request = info.context
		page = request.GET.get("page_old_private_image", 1)
		queryset = queryset.filter(type_action = "update")
		paginator = paginator_function(queryset, 5, page)
		return paginator


class ImagePrivateUserType(DjangoObjectType):
	class Meta:
		model = ImagePrivateUserModel
		fields = (
				 "avatar",
				 "identity_card",
				 "student_card",
				 "create_at",
				 )

	def resolve_identity_card(self, info):
		if is_owner(self, info):
			return self.identity_card

	def resolve_student_card(self, info):
		if is_owner(self, info):
			return self.student_card


class ImageOfUserType(DjangoObjectType):
	class Meta:
		model = ImageOfUserModel
		fields = (
				 "image",
				 "type_image",
				 "create_at",
				 "is_using",
				 )

	def resolve_image(self, info):
		if is_owner(self, info):
			return self.image
		elif self.is_public:
			return self.image
		else:
			return ''

	@classmethod
	def get_queryset(cls, queryset, info):
		request = info.context

		condition = Q(is_deleted=False)
		queryset = queryset.filter(condition)

		page = request.GET.get("page_image_of_user", 1)
		paginator = paginator_function(queryset, 10, page)
		return paginator


class ParentType(DjangoObjectType):
	class Meta:
		model = ParentModel
		fields = (
				  "first_name",
				  "last_name",
				  "birthday",

				  "province_code",
				  "district_code",
				  "ward_code",

				  # đia chỉ chi tiết cũng nhạy cảm
				  "detail_location",

				  # thông tin cực kì nhạy cảm
				  "number_phone",
				  "number_of_identity_card",

				  # các lớp mà phụ huynh tạo
				  "parentroommodel_set",

				  )


	# self là một đối tượng của ParentModel, không phải là đối tượng của ParentType

	def resolve_detail_location(self, info):
		if is_owner(self, info):
			return self.detail_location
	
	def resolve_number_phone(self, info):
		if is_owner(self, info):
			return self.number_phone

	def resolve_number_of_identity_card(self, info):
		if is_owner(self, info):
			return self.number_of_identity_card


class ParentRoomType(DjangoObjectType):
	class Meta:
		model = ParentRoomModel
		fields = (
				  "id",
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

				  # gia ca
				  "pricemodel_set",

				  # phụ huynh tạo ra lớp học
				  "parent",

				  # # comment ve lop hoc
				  # "commentaboutparentroommodel_set"

				  )
		convert_choices_to_enum = []


class OldLocationType(DjangoObjectType):
	class Meta:
		model = OldLocationModel


class PriceType(DjangoObjectType):
	class Meta:
		model = PriceModel

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


# for test
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
	# lay thong tin cua user
	get_user = graphene.Field(UserType, token=graphene.String(required=False))

	@login_required
	def resolve_get_user(root, info, **kwargs):
		request = info.context
		return User.objects.get(pk=request.user.id)

	# lay thong tin cua user public
	user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))

	def resolve_user_by_id(root, info, **kwargs):
		id = kwargs.get('id')
		return User.objects.get(pk=id)

	# # lấy thông tin của phụ huynh theo id  
	# parent_by_id = graphene.Field(ParentType, id=graphene.Int())

	# def resolve_parent_by_id(root, info, **kwargs):
	# 	id = kwargs.get("id");
	# 	return ParentModel.objects.get(pk=id)

	# # lấy thông tin của gia sư theo id
	# tutor_by_id = graphene.Field(TutorType, id=graphene.Int(), token=graphene.String(required=False))

	# def resolve_tutor_by_id(root, info, **kwargs):
	# 	id = kwargs.get("id");
	# 	return TutorModel.objects.get(pk=id)

	# lấy tất cả các lớp học
	all_room = graphene.List(ParentRoomType, page=graphene.Int(required=False))

	def resolve_all_room(root, info, **kwargs):
		page = kwargs.get("page", 1)

		return paginator_function(ParentRoomModel.objects.all(), 2, page)


schema = graphene.Schema(query=Query)
