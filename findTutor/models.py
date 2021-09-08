from django.db import models
from authentication.models import User
from multiselectfield import MultiSelectField

from .validators import min_code_of_location, max_code_of_province, max_code_of_district, max_code_of_ward
# Create your models here.

from django.conf import settings


# bảng gia sư
class TutorModel(models.Model):
    # nhạy cảm
    # mỗi người dùng chỉ được đăng kí một gia sư 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 

    # số thẻ căn cước công dân của gia sư
    # không yêu cầu cung cấp 
    # đây là dữ liệu nhạy cảm, chỉ gia sư và những người gia sư cho phép mới có thể thấy
    number_of_identity_card = models.CharField(null=True, blank=True, max_length=200)

    # số điện thoại
    # không yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ gia sư và những người gia sư cho phép mới có thể thấy
    number_phone = models.CharField(max_length=30, null=True, blank=True)

    # họ và tên
    # yêu cầu cung cấp
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)

    # ngày tháng năm sinh, YYYY-MM-DD
    # yêu cầu cung cấp
    birthday = models.DateField(null=False, blank=False)

    # đia chỉ của gia sư 
    # yêu cầu cung cấp, mã của tỉnh và mã của huyện
    # sử dụng mã code theo tiêu chuẩn của cuộc thống kê quốc gia Việt Nam
    province_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_province], default=1)
    district_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_district], default=1)
    ward_code = models.IntegerField(null=True, blank=True, validators=[min_code_of_location, max_code_of_ward], default=1)

    # địa chỉ chi tiết của gia sư (số nhà, đường, tổ, đội)
    # không yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ gia sư và những người gia sư cho phép mới có thể thấy 
    detail_location = models.CharField(max_length=500, null=True, blank=True)

    # nghề nghiệp hiện tại, một trong 2 lựa chọn (sinh viên hoặc giáo viên)
    # yêu cầu cung cấp 
    PROFESSION_CHOICES = [('sv', 'SINH_VIEN'), ('gv', 'GIAO_VIEN')]
    profession = models.CharField(max_length=10, choices=PROFESSION_CHOICES, null=False, blank=False)

    # trường đại học đã và đang học của gia sư
    # không yêu cầu cung cấp
    university = models.CharField(max_length=200, null=True, blank=True)

    # kinh nghiệm của gia sư
    # không yêu cầu cung cấp
    experience = models.TextField(null=True, blank=True) 

    # thành tích của gia sư
    # không yêu cầu cung cấp
    achievement = models.TextField(null=True, blank=True) 

    # các lớp gia sư dạy được
    # không yêu cầu cung cấp
    LOP_DAY_CHOICES = []
    for i in range(1, 18):
        LOP_DAY_CHOICES.append((i, i))
    lop_day = MultiSelectField(choices=LOP_DAY_CHOICES, min_choices=0)

    # khu vực có thể dạy của gia sư 
    # không yêu cầu cung cấp 
    khu_vuc_day = models.TextField(null=True, blank=True)

    # mon day
    mon_day = models.TextField(null=True, blank=True)

    CAP_DAY_CHOICES = []
    for i in range(1, 5):
        CAP_DAY_CHOICES.append((i, i))
    cap_day = MultiSelectField(choices=CAP_DAY_CHOICES, min_choices=0)

    @property
    def full_name(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


IS_BLANK_IMAGE_USER = True
AVATAR_FOLDER = "avatar/"   # thư mục lưu trữ ảnh đại diện
IDENTITY_CARD_FOLDER = "identity_card/"    # thư mục lưu trữ ảnh thẻ căn cước
STUDENT_CARD_FOLDER = "student_card/"   # thư mục lưu trữ ảnh thẻ sinh viên
OLD_IMAGE_PRIVATE_USER = 'old_image_private_user/'  # thư mục lưu trữ ảnh riêng tư cũ của user


class OldImagePrivateUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    if settings.USE_FIREBASE:
        image = models.TextField()
    else:
        image = models.ImageField()

    type_image_array = ['avatar', 'identity_card', 'student_card']
    type_image_choices = ((item, item) for item in type_image_array)
    type_image = models.CharField(max_length=200, choices=type_image_choices)

    type_action_array = ['update', 'delete']
    type_action_choices = ((item, item) for item in type_action_array)
    type_action = models.CharField(max_length=200, choices=type_action_choices)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_image + " cua " + self.user.username + " bi " + self.type_action


class ImagePrivateUserModel(models.Model):
    # mỗi người dùng có thể có nhiều ảnh đại diện hoặc ảnh thẻ căn cước do có thể thay đổi
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # ảnh đại diện của người dùng
    # không yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ người dùng và những người người dùng cho phép mới có thể thấy
    if settings.USE_FIREBASE:
        avatar = models.TextField(null=True, blank=True)
    else:
        avatar = models.ImageField(upload_to=AVATAR_FOLDER ,null=True, blank=IS_BLANK_IMAGE_USER)

    # ảnh thẻ căn cước của người dùng
    # không yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ người dùng và những người người dùng cho phép mới có thể thấy
    if settings.USE_FIREBASE:
        identity_card = models.TextField(null=True, blank=True)
    else:
        identity_card = models.ImageField(upload_to=IDENTITY_CARD_FOLDER ,null=True, blank=IS_BLANK_IMAGE_USER)

    # ảnh thẻ sinh viên
    # không yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ người dùng và những người người dùng cho phép mới có thể thấy
    if settings.USE_FIREBASE:
        student_card = models.TextField(null=True, blank=True)
    else:
        student_card = models.ImageField(upload_to=STUDENT_CARD_FOLDER, null=True, blank=IS_BLANK_IMAGE_USER)

    # thời gian tải lên
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


IMAGE_OF_USER_FOLDER = "user_image/"


class ImageOfUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # ảnh 
    # yêu cầu cung cấp
    if settings.USE_FIREBASE:
        image = models.TextField(null=True, blank=True)
    else: 
        image = models.ImageField(upload_to=IMAGE_OF_USER_FOLDER, null=False, blank=False)

    # loại của ảnh
    # không yêu cầu cung cấp
    type_image = models.CharField(max_length=200, null=True, blank=True)

    # thời gian tạo
    create_at = models.DateTimeField(auto_now_add=True)

    # người khác có thể xem được không
    is_public = models.BooleanField(default=True)

    # cho biet la anh cu hay anh moi
    is_using = models.BooleanField(default=True)

    # cho biet day co phai la anh nguoi dung da xoa hay khong
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.type_image + " cua " + self.user.username


from django.db.models.signals import pre_delete, pre_save, post_save

def before_image_private_user_delete(sender, instance, **kwargs):
    array_item = []

    if instance.avatar:
        old_avatar = OldImagePrivateUserModel()
        old_avatar.image = instance.avatar
        old_avatar.type_image = OldImagePrivateUserModel.type_image_array[0]    # avatar
        array_item.append(old_avatar)

    if instance.identity_card:
        old_identity_card = OldImagePrivateUserModel()
        old_identity_card.image = instance.identity_card
        old_identity_card.type_image = OldImagePrivateUserModel.type_image_array[1] # identity_card
        array_item.append(old_identity_card)

    if instance.student_card:
        old_student_card = OldImagePrivateUserModel()
        old_student_card.image = instance.student_card
        old_student_card.type_image = OldImagePrivateUserModel.type_image_array[2]  # student_card
        array_item.append(old_student_card)

    for item in array_item:
        item.type_action = OldImagePrivateUserModel.type_action_array[1]
        item.user = instance.user
        item.save()

    print("ban luu thanh cong")

pre_delete.connect(before_image_private_user_delete, sender=ImagePrivateUserModel)

def before_image_of_user_delete(sender, instance, **kwargs):
    old_image = ImageOfUserModel()
    old_image.image = instance.image
    old_image.user = instance.user
    old_image.type_image = instance.type_image
    old_image.is_public = False
    old_image.is_using = False
    old_image.is_deleted = True
    old_image.save()

pre_delete.connect(before_image_of_user_delete, sender=ImageOfUserModel)

class ParentModel(models.Model):
    # nhạy cảm
    # mỗi người dùng chỉ được đăng kí một gia sư
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # số điện thoại
    # không yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ gia sư và những người gia sư cho phép mới có thể thấy
    number_phone = models.CharField(max_length=30, null=True, blank=True)

    # số thẻ căn cước công dân của gia sư
    # không yêu cầu cung cấp 
    # đây là dữ liệu nhạy cảm, chỉ gia sư và những người gia sư cho phép mới có thể thấy
    number_of_identity_card = models.CharField(null=True, blank=True, max_length=200)

    # họ và tên
    # yêu cầu cung cấp
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)

    # ngày tháng năm sinh, YYYY-MM-DD
    # yêu cầu cung cấp
    birthday = models.DateField(null=True, blank=True)

    # đia chỉ của gia sư 
    # yêu cầu cung cấp mã của tỉnh và mã của huyện
    # sử dụng mã code theo tiêu chuẩn của cuộc thống kê quốc gia Việt Nam
    province_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_province], default=1)
    district_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_district], default=1)
    ward_code = models.IntegerField(null=True, blank=True, validators=[min_code_of_location, max_code_of_ward], default=1)

    # địa chỉ chi tiết của gia sư (số nhà, đường, tổ, đội)
    # không yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ gia sư và những người gia sư cho phép mới có thể thấy
    detail_location = models.CharField(max_length=500, null=True, blank=True)

    @property
    def full_name(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class ParentRoomModel(models.Model):
    # phụ huynh tạo ra lớp học
    # một phụ huynh có thể tao ra nhiều lớp học
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)

    # đia chỉ của gia sư 
    # yêu cầu cung cấp 
    # sử dụng mã code theo tiêu chuẩn của cuộc thống kê quốc gia Việt Nam
    province_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_province], default=1)
    district_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_district], default=1)
    ward_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_ward], default=1)

    # địa chỉ chi tiết của gia sư (số nhà, đường, tổ, đội)
    # yêu cầu cung cấp
    # đây là dữ liệu nhạy cảm, chỉ gia sư và những người gia sư cho phép mới có thể thấy
    detail_location = models.CharField(max_length=500, null=True, blank=True)

    # môn học
    # yêu cầu cung cấp
    subject = models.CharField(max_length=200, null=False, blank=False)

    # lớp 
    # yêu cầu cung cấp
    LOP_CHOICES = []
    for i in range(1, 18):
        if i <= 12:
            ten_lop = 'lop_' + str(i)
        else:
            ten_lop = 'nam_' + str(i-12)
        LOP_CHOICES.append((i, i))
    lop = models.IntegerField(choices=LOP_CHOICES, null=False, blank=False)

    # lớp học đã có người dạy hay chưa 
    isTeaching = models.BooleanField(default=False)

    # thời gian tạo lớp học
    create_at = models.DateTimeField(auto_now=True)

    # các ngày có thể dạy
    # yêu cầu cung cấp ít nhất một ngày
    DAY_CAN_TEACH_CHOICES = []
    for i in range(2, 9):
        if i <= 7:
            ten_ngay = 'thu_' + str(i)
        else:
            ten_ngay = 'chu_nhat'
        DAY_CAN_TEACH_CHOICES.append((i, i))
    day_can_teach = MultiSelectField(choices=DAY_CAN_TEACH_CHOICES, min_choices=1)

    # các yêu cầu đối với người dạy 
    # không yêu cầu cung cấp 
    other_require = models.TextField(null=True, blank=True)

    def get_max_price(self):
        pass

    def __str__(self):
        return 'lop ' + str(self.subject)


class OldLocationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    province_code = models.IntegerField(null=False, validators=[min_code_of_location, max_code_of_province], default=1)
    district_code = models.IntegerField(null=False, validators=[min_code_of_location, max_code_of_district], default=1)
    ward_code = models.IntegerField(null=True, validators=[min_code_of_location, max_code_of_ward], default=1)

    detail_location = models.CharField(max_length=500, null=False)

    create_at = models.DateTimeField(auto_now_add=True)


class PriceModel(models.Model):
    parent_room = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)

    time_in_one_day = models.DecimalField(max_digits=2, decimal_places=1, null=False)  # (hour)
    money_per_day = models.IntegerField(null=False)

    TEACHER_CHOICES = [('sv', 'Sinh Vien'), ('gv', 'Giao Vien')]
    type_teacher = MultiSelectField(choices=TEACHER_CHOICES, min_choices=1, null=False)

    SEX_OF_TEACHER_CHOICES = [('nu', 'NU'), ('nam', 'NAM')]
    sex_of_teacher = MultiSelectField(choices=SEX_OF_TEACHER_CHOICES, min_choices=1, null=False)

    def __str__(self):
        return str(self.parent_room) + ' : ' + str(self.time_in_one_day) +' tieng/buoi' +' : ' + str(self.money_per_day) + ' / buoi' + " cho gia su: " + str(self.sex_of_teacher) + ' ' + str(self.type_teacher)


class WaitingTutorModel(models.Model):
    parent_room = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    time_expired = models.BooleanField(default=False)
    parent_invite = models.BooleanField(default=False)


class ListInvitedModel(models.Model):
    tutor = models.ForeignKey(TutorModel, on_delete=models.CASCADE)
    parent_room = models.ForeignKey(ParentRoomModel, on_delete=models.CASCADE)
    tutor_agree = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)


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
    create_at = models.DateTimeField(auto_now_add=True)

