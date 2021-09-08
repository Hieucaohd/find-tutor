import graphene
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required

from .models import *
from authentication.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

from search.views import SearchShow

search_instance = SearchShow()


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
				  )


class TutorType(DjangoObjectType):
	class Meta:
		model = TutorModel
		fields =  (
				  "id",
				  "first_name", 
				  "last_name",
				  "birthday",

				  "province_code", 
				  "district_code", 
				  "ward_code",

				  # đia chỉ chi tiết cũng nhạy cảm
				  # private
				  "detail_location",

				  "profession",
				  "university",
				  "experience",
				  "achievement",
				  "lop_day",
				  "khu_vuc_day",

				  # thông tin cực kì nhạy cảm
				  # private
				  "number_phone",
				  #	private
				  "number_of_identity_card",

				  # thong tin ve lop
				  'waitingtutormodel_set',
				  'listinvitedmodel_set',
				  'tryteachingmodel_set',
				  'tutorteachingmodel_set',
				  )
		convert_choices_to_enum = []


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
				 "id",

				 # type = avatar => public
				 # type = identity_card, student_card => private
				 "image",
				 "type_image",
				 "type_action",
				 "create_at",
				 )

		convert_choices_to_enum = []

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
				 "id",

				 # public
				 "avatar",

				 # private
				 "identity_card",

				 # private
				 "student_card",
				 "create_at",
				 )
		convert_choices_to_enum = []

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
				 "id",
				 "image",
				 "type_image",
				 "create_at",
				 "is_using",
				 "is_public",
				 )
		convert_choices_to_enum = []

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
				  "id",
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
		convert_choices_to_enum = []


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

				  # thong tin cac danh sach
				  "waitingtutormodel_set",
				  "listinvitedmodel_set",
				  "tryteachingmodel",
				  "tutorteachingmodel",

				  # phụ huynh tạo ra lớp học
				  "parent",

				  )
		convert_choices_to_enum = []


class OldLocationType(DjangoObjectType):
	class Meta:
		model = OldLocationModel

		convert_choices_to_enum = []


class PriceType(DjangoObjectType):
	class Meta:
		model = PriceModel
		fields = (
				 "id",
				 "parent_room",
				 "time_in_one_day",
				 "money_per_day",
				 "type_teacher",
				 "sex_of_teacher",
				 )
		convert_choices_to_enum = []

class WaitingTutorType(DjangoObjectType):
	class Meta:
		model = WaitingTutorModel
		fields = (
				 "id",
				 "parent_room",
				 "tutor",
				 "create_at",
				 "time_expired",
				 "parent_invite",
				 )
		convert_choices_to_enum = []

class ListInvitedType(DjangoObjectType):
	class Meta:
		model = ListInvitedModel
		fields = (
				 "id",
				 "tutor",
				 "parent_room",
				 "tutor_agree",
				 "create_at"
				 )
		convert_choices_to_enum = []

class TryTeachingType(DjangoObjectType):
	class Meta:
		model = TryTeachingModel
		fields = (
				 "id",
				 "tutor",
				 "parent_room",
				 "tutor_agree",
				 "parent_agree",
				 "create_at",
				 "time_expired",
				 )
		convert_choices_to_enum = []

class TutorTeachingType(DjangoObjectType):
	class Meta:
		model = TutorTeachingModel
		fields = (
				 "id",
				 "tutor",
				 "parent_room",
				 "create_at",
				 )
		convert_choices_to_enum = []


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

class ResolveSearch:
	def __init__(self, model, fields, kwargs):
		self.model = model
		self.fields = fields
		self.kwargs = kwargs

		self.list_query = []

		self.get_location_query()

	def get_location_query(self):
		province_code = self.kwargs.get('province_code')
		district_code = self.kwargs.get('district_code')
		ward_code = self.kwargs.get('ward_code')

		if ward_code:
			self.list_query.append(Q(ward_code=ward_code))
		elif district_code:
			self.list_query.append(Q(district_code=district_code))
		elif province_code:
			self.list_query.append(Q(province_code=province_code))

	def resolve_search(self):

		search_infor = self.kwargs.get('search_infor')

		if search_infor:
			search_infor = search_instance.normal_search_infor(search_infor)
			return search_instance.search_engine(model=self.model, list_query=self.list_query, search_infor=search_infor, fields=self.fields)
		else:
			return search_instance.search_with_no_search_infor(model=self.model, list_query=self.list_query)


class ResolveSearchForRoom(ResolveSearch):

	def __init__(self, model, fields, kwargs):
		# call super init
		ResolveSearch.__init__(self, model=model, fields=fields, kwargs=kwargs)

		self.get_price_query()
		self.get_type_teacher_query()
		self.get_sex_of_teacher_query()
		self.get_lop_query()

	@staticmethod
	def normal_search_infor(search_infor):
		if search_infor:
			search_infor = search_instance.normal_search_infor(search_infor)

			replace_what = [{'word_replace': 'mon ', 'with': ''}, 
	                    	{'word_replace': ' hoc', 'with': ''}]

			for item in replace_what:
				search_infor = search_infor.replace(item.get('word_replace'), item.get('with'))

		return search_infor

	def get_price_query(self):
		price = self.kwargs.get('price')
		if len(price) >= 2:
			min_price = min(price)
			max_price = max(price)

			self.list_query.append(Q(pricemodel__money__gte=min_price) & Q(pricemodel__money__lte=max_price))

	def get_type_teacher_query(self):
		type_teachers = self.kwargs.get('type_teacher')
		type_teacher_query = Q()
		if type_teachers:
			for type_teacher in type_teachers:
				type_teacher_query &= Q(pricemodel__type_teacher__icontains=type_teacher)
			self.list_query.append(type_teacher_query)


	def get_sex_of_teacher_query(self):
		sex_of_teacher = self.kwargs.get('sex_of_teacher')
		if sex_of_teacher:
			self.list_query.append(Q(pricemodel__sex_of_teacher__icontains=sex_of_teacher))

	def get_lop_query(self):
		lops = self.kwargs.get("lop")
		lop_query = Q()
		if lops:
			for lop in lops:
				lop_query |= Q(lop=lop)
			self.list_query.append(lop_query)

	def resolve_search(self):

		search_infor = self.kwargs.get('search_infor')

		if search_infor:
			search_infor = self.normal_search_infor(search_infor)
			return search_instance.search_engine(model=self.model, list_query=self.list_query, search_infor=search_infor, fields=self.fields)
		else:
			return search_instance.search_with_no_search_infor(model=self.model, list_query=self.list_query)



class ResolveSearchForTutor(ResolveSearch):
	def __init__(self, model, fields, kwargs):
		# call parent init
		ResolveSearch.__init__(self, model=model, fields=fields, kwargs=kwargs)

		self.get_lop_query()

	def get_lop_query(self):
		lops = self.kwargs.get("lop")
		lop_query = Q()
		if lops:
			for lop in lops:
				lop_query |= Q(lop_day__icontains=str(lop))
			self.list_query.append(lop_query)


class ResolveSearchForParent(ResolveSearch):
	pass


class Query(graphene.ObjectType):

	# lấy thông tin của user qua id
	user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))

	def resolve_user_by_id(root, info, **kwargs):
		id = kwargs.get('id')
		# who_is(info.context)
		return User.objects.get(pk=id)

	"""
	lấy danh sach các lớp học
	sẽ chia ra thành các page, mỗi page sẽ có 16 lớp
	"""
	all_room = graphene.List(ParentRoomType, page=graphene.Int(required=False))

	def resolve_all_room(root, info, **kwargs):
		page = kwargs.get("page", 1)

		return paginator_function(ParentRoomModel.objects.all(), 16, page)

	# tim kiem lop hoc
	search_room = graphene.List(ParentRoomType, province_code = graphene.Int(required=False),
												district_code = graphene.Int(required=False),
												ward_code	  = graphene.Int(required=False),
												lop 		  = graphene.List(graphene.Int, required=False),
												price 		  = graphene.List(graphene.Int, required=False),
												sex_of_teacher= graphene.String(required=False),
												type_teacher  = graphene.List(graphene.String, required=False),
												search_infor  = graphene.String(required=False),
								)

	def resolve_search_room(root, info, **kwargs):

		def fields(item):
			return [item.subject, item.other_require]

		search_room = ResolveSearchForRoom(model=ParentRoomModel, fields=fields, kwargs=kwargs)

		return search_room.resolve_search()

	# tim kiem gia su
	search_tutor = graphene.List(TutorType, province_code = graphene.Int(required=False),
											district_code = graphene.Int(required=False),
											ward_code	  = graphene.Int(required=False),
											lop 		  = graphene.List(graphene.Int, required=False),
											search_infor  = graphene.String(required=False),
								)

	def resolve_search_tutor(root, info, **kwargs):

		def fields(item):
			return [item.full_name, item.experience, item.achievement, item.university, item.profession]

		search_tutor = ResolveSearchForTutor(model=TutorModel, fields=fields, kwargs=kwargs)

		return search_tutor.resolve_search()

	# tim kiem phu huynh
	search_parent = graphene.List(ParentType, province_code = graphene.Int(required=False),
											  district_code = graphene.Int(required=False),
											  ward_code	    = graphene.Int(required=False),
											  search_infor  = graphene.String(required=False),
								)

	def resolve_search_parent(root, info, **kwargs):
		def fields(item):
			return [item.full_name]

		search_parent = ResolveSearchForParent(model=ParentModel, fields=fields, kwargs=kwargs)

		return search_parent.resolve_search()


schema = graphene.Schema(query=Query, auto_camelcase=False)
