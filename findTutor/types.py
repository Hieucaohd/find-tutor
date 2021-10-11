import graphene
from graphene_django import DjangoObjectType

from django.db.models import Q

from findTutor.models import *

from findTutor.paginator import paginator_function


def is_owner(record_item, info):
    owner = info.context.user
    return record_item.user == owner

# permissions for tutor to see infor about parent
# def for_tutor_in_try_teaching(parent, info):
#     user_of_tutor = info.context.user
#     return parent.parentroommodel_set.filter(tryteachingmodel__tutor__user = user_of_tutor).exists()

def for_tutor_in_teaching(parent, info):
    user_of_tutor = info.context.user
    return parent.parentroommodel_set.filter(tutorteachingmodel__tutor__user = user_of_tutor).exists()

# permissions for parent to see infor about tutor
# def for_parent_in_try_teaching(tutor, info):
#     user_of_parent = info.context.user
#     return tutor.tryteachingmodel_set.filter(parent_room__parent__user = user_of_parent).exists()

def for_parent_in_waiting_list(tutor, info):
    user_of_parent = info.context.user
    return tutor.waitingtutormodel_set.filter(parent_room__parent__user = user_of_parent).exists()

def for_parent_in_teaching(tutor, info):
    user_of_parent = info.context.user
    return tutor.tutorteachingmodel_set.filter(parent_room__parent__user = user_of_parent).exists()



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
                  # private
                  "number_of_identity_card",

                  # thong tin lop hoc
                  'lop_day',
                  'cap_day',

                  # thong tin ve lop
                  'waitingtutormodel_set',
                  'listinvitedmodel_set',
                  'tryteachingmodel_set',
                  'tutorteachingmodel_set',

                  # user
                  'user',
                  )
        convert_choices_to_enum = []


    # self là một đối tượng của TutorModel, không phải là đối tượng của TutorType

    
    def resolve_detail_location(self, info):
        if ( is_owner(self, info) or 
             for_parent_in_waiting_list(self, info) or 
             for_parent_in_teaching(self, info) ):
            return self.detail_location
    
    def resolve_number_phone(self, info):
        if ( is_owner(self, info) or 
             for_parent_in_waiting_list(self, info) or
             for_parent_in_teaching(self, info) ):
            return self.number_phone

    def resolve_number_of_identity_card(self, info):
        if is_owner(self, info):
            return self.number_of_identity_card

    number_waiting = graphene.Int()
    
    def resolve_number_waiting(root, info, **kwargs):
        return WaitingTutorModel.objects.filter(tutor__id=root.id).count()

    number_invited = graphene.Int()

    def resolve_number_invited(root, info, **kwargs):
        return ListInvitedModel.objects.filter(tutor__id=root.id).count()

    number_try_teaching = graphene.Int()

    def resolve_number_try_teaching(root, info, **kwargs):
        return TryTeachingModel.objects.filter(tutor__id=root.id).count()

    number_teaching = graphene.Int()

    def resolve_number_teaching(root, info, **kwargs):
        return TutorTeachingModel.objects.filter(tutor__id=root.id).count()


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
                 "user",
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
    def get_queryset(cls, queryset, info, **kwargs):
        print(cls)
        print(dir(cls))
        print(cls.__doc__)
        print("kwargs =", kwargs)

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

                  # user
                  'user',
                  )
        convert_choices_to_enum = []


    # self là một đối tượng của ParentModel, không phải là đối tượng của ParentType

    def resolve_detail_location(self, info):
        if ( is_owner(self, info) or 
             for_tutor_in_teaching(self, info) ):
            return self.detail_location
    
    def resolve_number_phone(self, info):
        if ( is_owner(self, info) or 
             for_tutor_in_teaching(self, info) ):
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
                  "tryteachingmodel_set",
                  "tutorteachingmodel",

                  # phụ huynh tạo ra lớp học
                  "parent",
                  )
        convert_choices_to_enum = []

    number_waiting = graphene.Int()
    
    def resolve_number_waiting(root, info, **kwargs):
        return WaitingTutorModel.objects.filter(parent_room__id=root.id).count()

    number_invited = graphene.Int()

    def resolve_number_invited(root, info, **kwargs):
        return ListInvitedModel.objects.filter(parent_room__id=root.id).count()

    number_try_teaching = graphene.Int()

    def resolve_number_try_teaching(root, info, **kwargs):
        return TryTeachingModel.objects.filter(parent_room__id=root.id).count()

    number_tutor_teaching = graphene.Int()

    def resolve_number_tutor_teaching(root, info, **kwargs):
        try:
            tutor_teaching = root.tutorteachingmodel
            return 1
        except AttributeError:
            return 0


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


class ResultAllRoom(graphene.ObjectType):
    result = graphene.List(ParentRoomType)
    num_pages = graphene.Int()

class ResultAllTutor(graphene.ObjectType):
    result = graphene.List(TutorType)
    num_pages = graphene.Int()
