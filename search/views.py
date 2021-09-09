from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from findTutor.serializers import TutorSerializer, ParentSerializer, ParentRoomSerializer
from findTutor.models import TutorModel, ParentModel, ParentRoomModel
from findTutor.checkTutorAndParent import isTutor, isParent

from django.conf import settings

from .models import SearchModel

from django.db.models import Q

from rapidfuzz import fuzz
import rapidfuzz
import pylcs
import re
import unidecode


class Search(APIView):

    def normal_search_infor(self, search_infor):
        search_infor = re.sub(r'[^\w\s]', '', search_infor)
        search_infor = search_infor.lower()
        list_word = search_infor.split()

        list_word_normal = (re.sub(r'[^\w\s]', '', word) for word in list_word)

        result = " ".join(list_word_normal)
        result = unidecode.unidecode(result)
        return result

    def test_for_string(self, source, have):
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

        return max_score

    
    def get_result_search_infor(self, search_infor='', fields=[]):
        max_result = max(self.test_for_string(search_infor, field) for field in fields)
        return max_result

    def get_list_result_sorted(self, query_set, search_infor, fields):
        list_result = list( {
                                'item':item, 
                                'result': self.get_result_search_infor(search_infor, fields(item))
                            } 
                            for item in query_set
                        )

        def get_result(item):
            return item.get('result')

        list_result.sort(key=get_result, reverse=True)

        list_item = (item.get('item') for item in list_result if item.get('result') > 40)

        return list_item

    def get_query_set(self, model, list_query):
        sum_query = Q()
        for query in list_query:
            sum_query &= query
        return model.objects.filter(sum_query)

    def search_engine(self, model, list_query, search_infor, fields):
        query_set = self.get_query_set(model, list_query)
        return self.get_list_result_sorted(query_set, search_infor, fields)

    def search_with_no_search_infor(self, model, list_query):
        return self.get_query_set(model, list_query)

    def get(self, request, format=None):
        province_code = request.query_params.get('province_code', 0)
        district_code = request.query_params.get('district_code', 0)
        ward_code = request.query_params.get('ward_code', 0)

        lop = request.query_params.get('lop', [])
        print(lop)
        if lop == '':
            lop = []
        elif lop != []:
            try:
                lop = lop.split(",")
                lop = list(int(item) for item in lop)
            except:
                return Response(status=status.HTTP_204_NO_CONTENT)

        type_search = request.query_params.get('type', '')  # quy ước với bên front end là: room hoặc people
        if not (type_search == 'room' or type_search == 'people'):
            return Response(status=status.HTTP_403_FORBIDDEN)

        search_infor = request.query_params.get('search', '')
        
        can_tim_kiem = f'''Can tim kiem: 
                            \tsearch: {search_infor}
                            \tlop: {lop}
                            \ttype: {type_search}
                            \tprovince: {province_code}
                            \tdistrict: {district_code}
                            \tward: {ward_code}'''
        print(can_tim_kiem)

        location_query = None
        if province_code or district_code or ward_code:

            if province_code == '':
                province_code = 0

            if district_code == '':
                district_code = 0

            if ward_code == '':
                ward_code = 0

            try:
                location_query = Q(province_code = int(province_code)) | Q(district_code = int(district_code)) | Q(ward_code = int(ward_code))
            except:
                return Response(status=status.HTTP_204_NO_CONTENT)

        if request.user.is_authenticated and search_infor:
            SearchModel.objects.create(user=request.user, content_search=search_infor)

        if type_search == 'room':

            def fields(item):
                return [item.subject, item.other_require]

            def field_lop(item):
                return [item.lop]

            list_room = []
            if search_infor:
                list_room = self.search_engine(ParentRoomModel, location_query, search_infor, fields, lop, field_lop)
            else:
                list_room = self.search_with_no_search_infor(ParentRoomModel, location_query, search_infor, fields, lop, field_lop)

            return ParentRoomSerializer(list_room, many=True).data
        elif type_search == 'people':

            # truong cua tutor
            def fields_tutor(item):
                return [item.full_name, item.experience, item.achievement, item.university, item.profession]

            def field_lop_tutor(item):
                return list(item.lop_day)

            # truong cua parent
            def fields_parent(item):
                return [item.full_name]

            def field_lop_parent(item):
                return list()

            list_tutor = []
            list_parent = []
            if search_infor:
                list_tutor  = self.search_engine(TutorModel , location_query, search_infor, fields_tutor , lop, field_lop_tutor)
                list_parent = self.search_engine(ParentModel, location_query, search_infor, fields_parent, lop, field_lop_parent)
            else:
                list_tutor  = self.search_with_no_search_infor(TutorModel , location_query, search_infor, fields_tutor , lop, field_lop_tutor)
                list_parent = self.search_with_no_search_infor(ParentModel, location_query, search_infor, fields_parent, lop, field_lop_parent)

            return Response({
                    'list_tutor': TutorSerializer(list_tutor, many=True).data,
                    'list_parent': ParentSerializer(list_parent, many=True).data,
                })


class SearchImprove(Search):
    def test_for_string(self, search_infor, have):
        """
        
        """
        
        if not have:
            return 0

        try:
            have = self.normal_search_infor(have)
        except Exception:
            pass

        is_testing = False

        if settings.DEBUG or is_testing:
            print(f'search_infor: {search_infor}')
            print(f'have: {have}\n')

        levenshtein_dis = rapidfuzz.string_metric.levenshtein(search_infor, have)

        common_substring= pylcs.lcs2(search_infor, have)
        common_substring_phan_tram = common_substring / len(search_infor) * 100

        common_subsequen = pylcs.lcs(search_infor, have)
        common_subsequen_phan_tram = common_subsequen / len(search_infor) * 100

        # thông số thử nghiệm:
        # hamming 
        limit_same_length_hamming = 2
        score_same_length_hamming = 1000

        # levenshtein same length
        limit_same_length_levenshtein = 3
        score_same_length_levenshtein = 300

        # substring same length
        limit_same_length_substring = 40 # phan tram
        score_same_length_substring = 2
        
        # levenshtein diff length
        limit_diff_length_levenshtein = 2
        score_diff_length_levenshtein = 50

        # substring diff length
        limit_diff_length_substring = 50 # phan tram
        score_diff_length_substring = score_same_length_substring * 0.8

        # subsequense
        limit_diff_length_subsequen = 40 # phan tram
        score_diff_length_subsequen = score_same_length_substring * 0.4
        # end

        hamming_dis = 0
        result = 0
        if len(search_infor) == len(have):
            hamming_dis = rapidfuzz.string_metric.hamming(search_infor, have)

            if settings.DEBUG or is_testing: print('same length')

            if hamming_dis <= limit_same_length_hamming:
                result = (limit_same_length_hamming + 1 - hamming_dis) * score_same_length_hamming
                if settings.DEBUG or is_testing: print('\thamming')
            elif levenshtein_dis <= limit_same_length_levenshtein:
                result = (limit_same_length_levenshtein + 1 - levenshtein_dis) * score_same_length_levenshtein
                if settings.DEBUG or is_testing: print('\tlevenshtein')
            elif common_substring_phan_tram >= limit_same_length_substring: 
                if settings.DEBUG or is_testing: print('\tsubstring')
                result = common_substring_phan_tram * score_same_length_substring
        else:
            # phan_tram_length = len(search_infor) / len(have)
            # compute_length = phan_tram_length * 100 if phan_tram_length < 1 else 1/phan_tram_length * 100

            if settings.DEBUG or is_testing: print('not same length')
            if levenshtein_dis <= limit_diff_length_levenshtein:
                if settings.DEBUG or is_testing: print('\tlevenshtein')
                result = (limit_diff_length_levenshtein + 1 - levenshtein_dis) * score_diff_length_levenshtein
            elif common_substring_phan_tram >= limit_diff_length_substring:
                if settings.DEBUG or is_testing: print('\tsubstring')
                result = common_substring_phan_tram * score_diff_length_substring
            elif common_subsequen_phan_tram >= limit_diff_length_subsequen:
                if settings.DEBUG or is_testing: print('\tsubsequen')
                result = common_subsequen_phan_tram * score_diff_length_subsequen

                
        if settings.DEBUG or is_testing: print(f'\t\tresult {result}\n')
        return result


class SearchShow(SearchImprove):
    pass

