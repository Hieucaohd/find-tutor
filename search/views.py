from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from findTutor.serializers import TutorSerializer, ParentSerializer, ParentRoomSerializer
from findTutor.models import TutorModel, ParentModel, ParentRoomModel
from findTutor.checkTutorAndParent import isTutor, isParent

from .models import SearchModel

from django.db.models import Q

from numba import jit


class Search(APIView):

    def normal_search_infor(self, search_infor):
        import re
        import unidecode

        search_infor = re.sub(r'[^\w\s]', '', search_infor)
        search_infor = search_infor.lower()
        list_word = search_infor.split()

        list_word_normal = (re.sub(r'[^\w\s]', '', word) for word in list_word)

        result = " ".join(list_word_normal)
        result = unidecode.unidecode(result)
        return result

    def test_for_string(self, source, have):
        from rapidfuzz import fuzz
        import pylcs

        print('source: ', source)
        print('have: ', have)

        result_1 = fuzz.ratio(source, have)
        result_1_1 = fuzz.ratio(self.normal_search_infor(source), self.normal_search_infor(have))
        print(f'ratio: {result_1}, {result_1_1}')

        result_2 = 0
        result_2_2 = 0

        len_no_space_have = len(self.normal_search_infor(have).replace(' ', ""))
        if len_no_space_have > 2:
            result_2 = fuzz.partial_ratio(source, have)
            result_2_2 = fuzz.partial_ratio(self.normal_search_infor(source), self.normal_search_infor(have))
        print(f'fuzz: {result_2}, {result_2_2}')

        result_3 = 0
        result_3_3 = 0
        if len(source) != 0:
            result_3 = pylcs.lcs2(self.normal_search_infor(source), self.normal_search_infor(have)) / len(source) * 100
            result_3_3 = pylcs.lcs(self.normal_search_infor(source), self.normal_search_infor(have)) / len(source) * 100
        print(f'pylcs: {result_3}, {result_3_3}')

        score = max(result_1, result_1_1, result_2, result_2_2, result_3, result_3_3)
        print('max score: ', score)

        limit = 75

        return (result_1 >= limit) or \
               (result_1_1 >= limit) or \
               (result_2 >= limit) or \
               (result_2_2 >= limit) or \
               (result_3 >= limit) or \
               (result_3_3 >= limit)

    
    def condition_for_search_infor(self, search_infor='', fields=[]):
        for field in fields:
            if self.test_for_string(search_infor, field):
                return True
        return False

    def condition_for_lop(self, lop=[], field_lop=[]):
        set_1 = set(lop)
        set_2 = set(field_lop)

        if (set_1 & set_2):
            return True
        else:
            return False

    def condition(self, search_infor='', fields=[], lop=[], field_lop=[]):
        if lop:
            return self.condition_for_search_infor(search_infor, fields) and self.condition_for_lop(lop, field_lop)
        else:
            return self.condition_for_search_infor(search_infor, fields)

    def search_engine(self, model, serializer, location_query, search_infor, fields, lop, field_lop):
        list_result = []

        if location_query:
            list_result = (item for item in model.objects.filter(location_query) if 
                            self.condition(search_infor, fields(item), lop, field_lop(item)))
        else:
            list_result = (item for item in model.objects.all() if
                            self.condition(search_infor, fields(item), lop, field_lop(item)))

        data = serializer(list_result, many=True).data

        return data

    def get(self, request, format=None):
        province_code = request.query_params.get('province_code', 0)
        district_code = request.query_params.get('district_code', 0)
        ward_code = request.query_params.get('ward_code', 0)

        lop = request.query_params.get('lop', [])
        try:
            if lop != []:
                lop = lop.split(",")
                lop = list(int(item) for item in lop)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

        type_search = request.query_params.get('type', '')  # quy ước với bên front end là: room hoặc people

        search_infor = request.query_params.get('search', '')
        search_infor = self.normal_search_infor(search_infor)
        
        can_tim_kiem = f'''Can tim kiem: 
                            \tsearch: {search_infor}
                            \tlop: {lop}
                            \ttype: {type_search}
                            \tprovince: {province_code}
                            \tdistrict: {district_code}
                            \tward: {ward_code}'''
        print(can_tim_kiem)
        print('lop: ', lop[1])

        location_query = None
        if province_code or district_code or ward_code:
            location_query = Q(province_code = int(province_code)) | Q(district_code = int(district_code)) | Q(ward_code = int(ward_code))

        if request.user.is_authenticated:
            SearchModel.objects.create(user=request.user, content_search=search_infor)

        if type_search == 'room':

            def fields(item):
                return [item.subject, item.other_require]

            def field_lop(item):
                return [item.lop]

            return Response(self.search_engine(ParentRoomModel, ParentRoomSerializer, location_query, search_infor, fields, lop, field_lop))
        elif type_search == 'people':

            def fields_tutor(item):
                return [item.full_name, item.experience, item.achievement, item.university, item.profession]

            def field_lop_tutor(item):
                return list(item.lop_day)

            list_tutor  = self.search_engine(TutorModel , TutorSerializer , location_query, search_infor, fields_tutor , lop, field_lop_tutor)
            
            def fields_parent(item):
                return [item.full_name]

            def field_lop_parent(item):
                return list()

            list_parent = self.search_engine(ParentModel, ParentSerializer, location_query, search_infor, fields_parent, lop, field_lop_parent)

            return Response({
                    'list_tutor': list_tutor,
                    'list_parent': list_parent
                })





