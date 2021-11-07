from django.db import models

from .validators import (min_code_of_location, 
                         max_code_of_province, 
                         max_code_of_district, 
                         max_code_of_ward)


class BaseModel(models.Model):
    """
        Tất cả các model class trong project phải kế thừa từ class này
    """
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True



class CommonInfoAbstractModel(BaseModel):
    """
        Tất cả các model class mô tả về người phải kế thừa từ class này
    """

    number_phone = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    birthday = models.DateField(null=False, blank=False)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class CommonLocationAbstractModel(BaseModel):
    """
        Tất cả các model class muốn lưu trữ địa điểm phải kế thừa từ class này
    """

    # sử dụng mã code theo cung cấp của tổng cuc thống kê quốc gia Việt Nam
    province_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_province], default=1)
    district_code = models.IntegerField(null=False, blank=False, validators=[min_code_of_location, max_code_of_district], default=1)
    ward_code = models.IntegerField(null=True, blank=True, validators=[min_code_of_location, max_code_of_ward], default=1)

    detail_location = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True