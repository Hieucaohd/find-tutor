from django.core.exceptions import ValidationError
from vietnam_provinces.enums import ProvinceEnum, DistrictEnum
from vietnam_provinces.enums.wards import WardEnum

MAX_CODE_OF_PROVINCE = list(ProvinceEnum)[-1].value.code
MAX_CODE_OF_DISTRICT = list(DistrictEnum)[-1].value.code
MAX_CODE_OF_WARD = list(WardEnum)[-1].value.code


def min_code_of_location(value):
    if value < 1:
        raise ValidationError("gia tri code cua location khong the nho hon 1.")


def max_code_of_province(value):
    if value > MAX_CODE_OF_PROVINCE:
        raise ValidationError("gia tri code cua tinh, thanh pho khong the lon hon " + str(MAX_CODE_OF_PROVINCE))


def max_code_of_district(value):
    if value > MAX_CODE_OF_DISTRICT:
        raise ValidationError("gia tri code cua huyen, quan khong the lon hon " + str(MAX_CODE_OF_DISTRICT))


def max_code_of_ward(value):
    if value > MAX_CODE_OF_WARD:
        raise ValidationError("gia tri code cua xa, phuong khong the lon hon " + str(MAX_CODE_OF_WARD))