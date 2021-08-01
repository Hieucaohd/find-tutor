from django.db import models
from authentication.models import User
from multiselectfield import MultiSelectField

# Create your models here.


class UserPrimaryInformation(models.Model):
    # imagine
    avatar = models.ImageField(null=True)
    identity_card = models.ImageField(null=True)

    # information
    number_phone = models.CharField(max_length=30, null=True)
    number_of_identity_card = models.IntegerField(null=True)

    # name
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)

    birthday = models.DateField(null=True)
    location = models.CharField(max_length=200, null=True)

    def __str__(self):
        full_name = str(self.first_name) + ' ' + str(self.last_name)
        return full_name


class TutorModel(UserPrimaryInformation):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profession
    PROFESSION_CHOICES = [('sv', 'SINH_VIEN'), ('gv', 'GIAO_VIEN')]
    profession = models.CharField(max_length=10, choices=PROFESSION_CHOICES, null=True)
    university = models.CharField(max_length=200, null=True)

    experience = models.TextField(null=True)  #kinh nghiem
    achievement = models.TextField(null=True)  #thanh tich

    CAP_DAY_CHOICES = []
    for i in range(1, 5):
        ten_cap = 'cap_' + str(i)
        if i == 4:
            ten_cap = 'dai_hoc'
        CAP_DAY_CHOICES.append((i, ten_cap))
    cap_day = MultiSelectField(choices=CAP_DAY_CHOICES, null=True)

    LOP_DAY_CHOICES = []
    for i in range(1, 18):
        if i <= 12:
            ten_lop = 'lop_' + str(i)
        else:
            ten_lop = 'nam_' + str(i-12)
        LOP_DAY_CHOICES.append((i, ten_lop))
    lop_day = MultiSelectField(choices=LOP_DAY_CHOICES, null=True)

    khu_vuc_day = models.TextField(null=True)


class ParentModel(UserPrimaryInformation):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ParentRoomModel(models.Model):
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=False) # can select
    detail_location = models.CharField(max_length=500, null=True)

    subject = models.CharField(max_length=200, null=False)  # can select
    LOP_CHOICES = []
    for i in range(1, 18):
        if i <= 12:
            ten_lop = 'lop_' + str(i)
        else:
            ten_lop = 'nam_' + str(i-12)
        LOP_CHOICES.append((i, ten_lop))
    lop = models.IntegerField(choices=LOP_CHOICES, null=False)

    isTeaching = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True)

    DAY_CAN_TEACH_CHOICES = []
    for i in range(2, 9):
        if i <= 7:
            ten_ngay = 'thu_' + str(i)
        else:
            ten_ngay = 'chu_nhat'
        DAY_CAN_TEACH_CHOICES.append((i, ten_ngay))
    day_can_teach = MultiSelectField(choices=DAY_CAN_TEACH_CHOICES, min_choices=1)

    other_require = models.TextField(null=True)

    def __str__(self):
        return 'lop ' + str(self.subject)


class PriceModel(models.Model):
    parent_room = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)

    time_in_one_day = models.DecimalField(max_digits=2, decimal_places=1, null=False)  #(hour)
    money = models.IntegerField(null=False)
    PER_CHOICES = [
        ('buoi', 'BUOI'),
        ('tieng', 'TIENG'),
    ]
    time_price_pay_for = models.CharField(max_length=20, choices=PER_CHOICES, null=False)

    TEACHER_CHOICES = [('sv', 'Sinh Vien'), ('gv', 'Giao Vien')]
    teacher = models.CharField(choices=TEACHER_CHOICES, max_length=20, null=False)

    SEX_OF_TEACHER_CHOICES = [('nu', 'NU'), ('nam', 'NAM')]
    sex_of_teacher = MultiSelectField(choices=SEX_OF_TEACHER_CHOICES, min_choices=1, null=False)

    def __str__(self):
        return str(self.parent_room) + ' ' + str(self.money)


class WaitingTutorModel(models.Model):
    parent_room = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
    join_at = models.DateTimeField(auto_now_add=True)
    time_expired = models.BooleanField(default=False)
    parent_invite = models.BooleanField(default=False)
    # tutor_agree = models.BooleanField(default=False)


class ListInvitedModel(models.Model):
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
    parent_room = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)
    tutor_agree = models.BooleanField(default=False)


class TryTeachingModel(models.Model):
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
    parent_room = models.OneToOneField(ParentRoomModel, on_delete=models.CASCADE)
    tutor_agree = models.BooleanField(default=False)
    parent_agree = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    time_expired = models.BooleanField(default=False)


class TutorTeachingModel(models.Model):
    parent_room = models.OneToOneField(ParentRoomModel, on_delete=models.CASCADE)
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
    start_at = models.DateTimeField(auto_now_add=True)


class NotifiedModel(models.Model):
    content = models.TextField()
    notified_at = models.DateTimeField(auto_now_add=True)


class NotifiedParentModel(NotifiedModel):
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)


class NotifiedTutorModel(NotifiedModel):
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)


class CommentAboutTutorModel(models.Model):
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

