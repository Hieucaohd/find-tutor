from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from vietnam_provinces.enums import ProvinceEnum, DistrictEnum
from vietnam_provinces.enums.wards import WardEnum


######################################### Xác minh mã code của địa điểm ######################################
# Mã code cao nhất của tỉnh
MAX_CODE_OF_PROVINCE = list(ProvinceEnum)[-1].value.code

# Mã code cao nhất của huyện, thị xã
MAX_CODE_OF_DISTRICT = list(DistrictEnum)[-1].value.code

# Mã code cao nhất của xã, phường, thị trấn
MAX_CODE_OF_WARD = list(WardEnum)[-1].value.code


def min_code_of_location(value):
    """
        Mã code nhỏ nhất luôn là 1.
    """
    if value < 1:
        raise ValidationError(_("Value of location must greater than or equal 1"))


def max_code_of_province(value):
    if value > MAX_CODE_OF_PROVINCE:
        raise ValidationError(_(f"Value of province code must be less than or equal {MAX_CODE_OF_PROVINCE}"))


def max_code_of_district(value):
    if value > MAX_CODE_OF_DISTRICT:
        raise ValidationError(_(f"Value of district code must be less than or equal {MAX_CODE_OF_DISTRICT}"))


def max_code_of_ward(value):
    if value > MAX_CODE_OF_WARD:
        raise ValidationError(_(f"Value of ward code must be less than or equal {MAX_CODE_OF_WARD}"))