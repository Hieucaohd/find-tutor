from rest_framework import serializers, fields
from rest_framework.authtoken.models import Token
from authentication.models import User
from .models import *

from django.conf.settings import USE_FIREBASE


class TutorSerializer(serializers.ModelSerializer):

    CAP_DAY_CHOICES = TutorModel.CAP_DAY_CHOICES
    cap_day = serializers.MultipleChoiceField(choices=CAP_DAY_CHOICES)

    LOP_DAY_CHOICES = TutorModel.LOP_DAY_CHOICES
    lop_day = serializers.MultipleChoiceField(choices=LOP_DAY_CHOICES)

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = TutorModel
        fields = '__all__'

        extra_kwargs = {
            'cap_day': {
                'required': False,
            },
            'avatar': {
                'required': False,
            },
            'identity_card': {
                'required': False,
            },
            'lop_day': {
                'required': False,
            },
            'birthday': {
                'required': False,
            },
            'full_name': {
                'read_only': True,
            }
        }


class ImagePrivateUserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ImagePrivateUserModel
        fields = '__all__'

        extra_kwargs = {
            'avatar': {
                'required': False
            },
            'identity_card': {
                'required': False
            },
            'student_card': {
                'required': False
            }
        }

        if USE_FIREBASE:
            extra_kwargs = {
                'avatar': {
                    'required': False,
                    'read_only': True,
                },
                'identity_card': {
                    'required': False,
                    'read_only': True,
                },
                'student_card': {
                    'required': False,
                    'read_only': True,
                }
            }


class ImageOfUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='user.username', read_only="True")

    class Meta:
        model = ImageOfUserModel
        fields = '__all__'


class ParentSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ParentModel
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'read_only': True,
            },
            'avatar': {
                'required': False,
            },
            'identity_card': {
                'required': False,
            },
            'full_name': {
                'read_only': True,
            }
        }

DAY_CAN_TEACH_CHOICES = ParentRoomModel.DAY_CAN_TEACH_CHOICES

class ParentRoomSerializer(serializers.ModelSerializer):
    
    day_can_teach = serializers.MultipleChoiceField(choices=DAY_CAN_TEACH_CHOICES)

    parent = serializers.PrimaryKeyRelatedField(read_only='True', source='parent.user.id')

    class Meta:
        model = ParentRoomModel
        fields = '__all__'

        extra_kwargs = {
            'day_can_teach': {
                'required': False
            }
        }


class OldLocationSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only='True', source='parent.user.id')

    class Meta:
        model = OldLocationModel
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):

    SEX_OF_TEACHER_CHOICES = PriceModel.SEX_OF_TEACHER_CHOICES
    sex_of_teacher = serializers.MultipleChoiceField(choices=SEX_OF_TEACHER_CHOICES)

    parent_room = serializers.PrimaryKeyRelatedField(read_only='True', source='parent_room.id')

    class Meta:
        model = PriceModel
        fields = '__all__'

        extra_kwargs = {
            'sex_id_teacher': {
                'required': False,
            }
        }


class WaitingTutorSerializer(serializers.ModelSerializer):
    parent_room = serializers.PrimaryKeyRelatedField(read_only='True', source='parent_room.parent.user.id')
    
    tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    parent_invite = serializers.ReadOnlyField()
    tutor_agree = serializers.ReadOnlyField()

    roomId = serializers.IntegerField(read_only="True", source='parent_room.id')

    province_code = serializers.IntegerField(read_only="True", source='parent_room.province_code')
    district_code = serializers.IntegerField(read_only="True", source='parent_room.district_code')
    ward_code = serializers.IntegerField(read_only="True", source='parent_room.ward_code')
    
    detail_location = serializers.CharField(read_only="True", source='parent_room.detail_location')
    subject = serializers.CharField(read_only="True", source='parent_room.subject')  # can select
    lop = serializers.IntegerField(read_only="True", source='parent_room.lop')
    isTeaching = serializers.BooleanField(read_only="True", source='parent_room.isTeaching')
    create_at = serializers.DateTimeField(read_only="True", source='parent_room.create_at')
    day_can_teach = serializers.MultipleChoiceField(read_only="True", source='parent_room.day_can_teach', choices=DAY_CAN_TEACH_CHOICES)
    other_require = serializers.CharField(read_only="True", source='parent_room.other_require')

    class Meta:
        model = WaitingTutorModel
        fields = '__all__'


class ListInvitedSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    parent_room = serializers.PrimaryKeyRelatedField(read_only='True', source='parent_room.parent.user.id')
    #roomId = serializers.IntegerField(read_only="True", source="parent_room.id")
    tutor_agree = serializers.ReadOnlyField()

    roomId = serializers.IntegerField(read_only="True", source='parent_room.id')

    province_code = serializers.IntegerField(read_only="True", source='parent_room.province_code')
    district_code = serializers.IntegerField(read_only="True", source='parent_room.district_code')
    ward_code = serializers.IntegerField(read_only="True", source='parent_room.ward_code')
    
    detail_location = serializers.CharField(read_only="True", source='parent_room.detail_location')
    subject = serializers.CharField(read_only="True", source='parent_room.subject')  # can select
    lop = serializers.IntegerField(read_only="True", source='parent_room.lop')
    isTeaching = serializers.BooleanField(read_only="True", source='parent_room.isTeaching')
    create_at = serializers.DateTimeField(read_only="True", source='parent_room.create_at')
    day_can_teach = serializers.MultipleChoiceField(read_only="True", source='parent_room.day_can_teach', choices=DAY_CAN_TEACH_CHOICES)
    other_require = serializers.CharField(read_only="True", source='parent_room.other_require')

    class Meta:
        model = ListInvitedModel
        fields = '__all__'


class TryTeachingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    parent_room = serializers.ReadOnlyField(source='parent_room.parent.user.id')
    tutor_agree = serializers.ReadOnlyField()
    parent_agree = serializers.ReadOnlyField()

    roomId = serializers.IntegerField(read_only="True", source='parent_room.id')

    province_code = serializers.IntegerField(read_only="True", source='parent_room.province_code')
    district_code = serializers.IntegerField(read_only="True", source='parent_room.district_code')
    ward_code = serializers.IntegerField(read_only="True", source='parent_room.ward_code')
    
    detail_location = serializers.CharField(read_only="True", source='parent_room.detail_location')
    subject = serializers.CharField(read_only="True", source='parent_room.subject')  # can select
    lop = serializers.IntegerField(read_only="True", source='parent_room.lop')
    isTeaching = serializers.BooleanField(read_only="True", source='parent_room.isTeaching')
    create_at = serializers.DateTimeField(read_only="True", source='parent_room.create_at')
    day_can_teach = serializers.MultipleChoiceField(read_only="True", source='parent_room.day_can_teach', choices=DAY_CAN_TEACH_CHOICES)
    other_require = serializers.CharField(read_only="True", source='parent_room.other_require')

    class Meta:
        model = TryTeachingModel
        fields = '__all__'


class TutorTeachingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    parent_room = serializers.ReadOnlyField(source='parent_room.parent.user.id')

    roomId = serializers.IntegerField(read_only="True", source='parent_room.id')

    province_code = serializers.IntegerField(read_only="True", source='parent_room.province_code')
    district_code = serializers.IntegerField(read_only="True", source='parent_room.district_code')
    ward_code = serializers.IntegerField(read_only="True", source='parent_room.ward_code')
    
    detail_location = serializers.CharField(read_only="True", source='parent_room.detail_location')
    subject = serializers.CharField(read_only="True", source='parent_room.subject')  # can select
    lop = serializers.IntegerField(read_only="True", source='parent_room.lop')
    isTeaching = serializers.BooleanField(read_only="True", source='parent_room.isTeaching')
    create_at = serializers.DateTimeField(read_only="True", source='parent_room.create_at')
    day_can_teach = serializers.MultipleChoiceField(read_only="True", source='parent_room.day_can_teach', choices=DAY_CAN_TEACH_CHOICES)
    other_require = serializers.CharField(read_only="True", source='parent_room.other_require')

    class Meta:
        model = TutorTeachingModel
        fields = '__all__'
