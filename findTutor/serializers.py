from rest_framework import serializers, fields
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import *


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
            }
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
        }


class ParentRoomSerializer(serializers.ModelSerializer):
    DAY_CAN_TEACH_CHOICES = ParentRoomModel.DAY_CAN_TEACH_CHOICES
    day_can_teach = serializers.MultipleChoiceField(choices=DAY_CAN_TEACH_CHOICES)

    parent = serializers.PrimaryKeyRelatedField(read_only='True', source='parent.user.username')

    class Meta:
        model = ParentRoomModel
        fields = '__all__'

        extra_kwargs = {
            'day_can_teach': {
                'required': False
            }
        }


class PriceSerializer(serializers.ModelSerializer):

    SEX_OF_TEACHER_CHOICES = PriceModel.SEX_OF_TEACHER_CHOICES
    sex_of_teacher = serializers.MultipleChoiceField(choices=SEX_OF_TEACHER_CHOICES)

    class_id = serializers.PrimaryKeyRelatedField(read_only='True', source='class_id.parent.user.username')

    class Meta:
        model = PriceModel
        fields = '__all__'

        extra_kwargs = {
            'sex_id_teacher': {
                'required': False,
            }
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
