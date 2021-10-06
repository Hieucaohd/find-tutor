from rest_framework import serializers, fields
from rest_framework.authtoken.models import Token
from authentication.models import User
from .models import *

from django.conf import settings


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

        if settings.USE_FIREBASE:
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

        extra_kwargs = {
            "image": {
                "required": True,
            },
            "type_image": {
                "required": False,
            },
            "is_using": {
                "read_only": True,
            },
            "is_deleted": {
                "read_only": True,
            },
        }

        if settings.USE_FIREBASE:
            extra_kwargs = {
                "image": {
                    "read_only": True,
                },
                "type_image": {
                    "required": False,
                },
                "is_using": {
                    "read_only": True,
                },
                "is_deleted": {
                    "read_only": True,
                },
            }


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
    sex_of_teacher = serializers.MultipleChoiceField(choices=SEX_OF_TEACHER_CHOICES, required=False)

    TEACHER_CHOICES = PriceModel.TEACHER_CHOICES
    type_teacher = serializers.MultipleChoiceField(choices=TEACHER_CHOICES, required=False)

    parent_room = serializers.PrimaryKeyRelatedField(read_only='True', source='parent_room.id')

    class Meta:
        model = PriceModel
        fields = '__all__'

        extra_kwargs = {
            'sex_id_teacher': {
                'required': False,
            },
            'time_in_one_day': {
                'required': False
            }
        }


class WaitingTutorSerializer(serializers.ModelSerializer):
    parent_room = serializers.PrimaryKeyRelatedField(read_only='True', source='parent_room.parent.user.id')
    
    # tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    tutor = TutorSerializer()
    parent_invite = serializers.ReadOnlyField()

    class Meta:
        model = WaitingTutorModel
        fields = '__all__'


class ListInvitedSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    parent_room = serializers.PrimaryKeyRelatedField(read_only='True', source='parent_room.parent.user.id')

    tutor_agree = serializers.ReadOnlyField()

    class Meta:
        model = ListInvitedModel
        fields = '__all__'


class TryTeachingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    parent_room = serializers.ReadOnlyField(source='parent_room.parent.user.id')

    tutor_agree = serializers.ReadOnlyField()
    parent_agree = serializers.ReadOnlyField()

    class Meta:
        model = TryTeachingModel
        fields = '__all__'


class TutorTeachingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(read_only='True', source='tutor.user.id')
    parent_room = serializers.ReadOnlyField(source='parent_room.parent.user.id')

    class Meta:
        model = TutorTeachingModel
        fields = '__all__'
