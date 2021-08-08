from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from findTutor.serializers import TutorSerializer, ParentSerializer, ParentRoomSerializer
from findTutor.models import TutorModel, ParentModel, ParentRoomModel
from findTutor.checkTutorAndParent import isTutor, isParent

from .models import SearchModel

from django.db.models import Q


class Search(APIView):

    def normal_search_infor(self, search_infor):
        import re
        import unidecode

        search_infor = re.sub(r'[^\w\s]', '', search_infor)
        search_infor = search_infor.lower()
        list_word = search_infor.split()

        # list_word_normal = []
        # for word in list_word:
        #     word = re.sub(r'[^\w\s]', '', word)
        #     list_word_normal.append(word)

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

        # len_no_space_1 = len(self.normal_search_infor(source).replace(' ', ""))
        # len_no_space_2 = len(self.normal_search_infor(have).replace(' ', ""))
        # sum_of_word = 0
        # if len_no_space_1 > len_no_space_2:
        #     sum_of_word =  len_no_space_2 / len_no_space_1
        # else:
        #     sum_of_word = len_no_space_1 / len_no_space_2

        # print(f'sum of word: {sum_of_word}')

        # if sum_of_word > 0.7:

        len_no_space_have = len(self.normal_search_infor(have).replace(' ', ""))
        if len_no_space_have > 2:
            result_2 = fuzz.partial_ratio(source, have)
            result_2_2 = fuzz.partial_ratio(self.normal_search_infor(source), self.normal_search_infor(have))
        print(f'fuzz: {result_2}, {result_2_2}')

        result_3 = pylcs.lcs2(self.normal_search_infor(source), self.normal_search_infor(have)) / len(source) * 100
        result_3_3 = pylcs.lcs(self.normal_search_infor(source), self.normal_search_infor(have)) / len(source) * 100
        print(f'pylcs: {result_3}, {result_3_3}')

        # score = max(result_1, result_1_1, result_2, result_2_2, result_3, result_3_3)
        # print(score)

        limit = 75

        return (result_1 >= limit) or \
               (result_1_1 >= limit) or \
               (result_2 >= limit) or \
               (result_2_2 >= limit) or \
               (result_3 >= limit) or \
               (result_3_3 >= limit)

    def search_parent(self, request, search_infor, q_object):

        list_parent = []
        if q_object:
            list_parent = (parent for parent in ParentModel.objects.filter(q_object) if
                            self.test_for_string(search_infor, parent.full_name))
        else:
            list_parent = (parent for parent in ParentModel.objects.all() if
                            self.test_for_string(search_infor, parent.full_name))

        data_parent = ParentSerializer(list_parent, many=True)

        return data_parent.data

    def search_tutor(self, request, search_infor, q_object):

        list_tutor = []
        if q_object:
            list_tutor = (tutor for tutor in TutorModel.objects.filter(q_object) if
                          self.test_for_string(search_infor, tutor.full_name) or
                          self.test_for_string(search_infor, tutor.experience) or
                          self.test_for_string(search_infor, tutor.achievement) or 
                          self.test_for_string(search_infor, tutor.university))
        else:
            list_tutor = (tutor for tutor in TutorModel.objects.all() if
                          self.test_for_string(search_infor, tutor.full_name) or
                          self.test_for_string(search_infor, tutor.experience) or
                          self.test_for_string(search_infor, tutor.achievement) or 
                          self.test_for_string(search_infor, tutor.university))

        data_tutor = TutorSerializer(list_tutor, many=True)

        return data_tutor.data

    def search_for_room(self, request, search_infor, q_object):

        list_parent_room = []
        if q_object:
            list_parent_room = (room for room in ParentRoomModel.objects.filter(q_object) if
                                self.test_for_string(search_infor, room.subject) or
                                self.test_for_string(search_infor, room.other_require))
        else:
            list_parent_room = (room for room in ParentRoomModel.objects.all() if
                                self.test_for_string(search_infor, room.subject) or
                                self.test_for_string(search_infor, room.other_require))

        data_parent_room = ParentRoomSerializer(list_parent_room, many=True)

        return Response(data_parent_room.data)

    def get(self, request, format=None):
        province_code = request.query_params.get('province_code', 0)
        district_code = request.query_params.get('district_code', 0)
        ward_code = request.query_params.get('ward_code', 0)

        #room = request.query_params.get('room', 0)
        type_search = request.query_params.get('type', '')  # quy ước với bên front end là: room hoặc people

        search_infor = request.query_params.get('search', '')
        search_infor = self.normal_search_infor(search_infor)
        print(search_infor)

        q_object = ''
        if province_code or district_code or ward_code:
            q_object = Q(province_code = int(province_code)) | Q(district_code = int(district_code)) | Q(ward_code = int(ward_code))
        
        # if room:
        #     return self.search_for_room(request, search_infor, q_object)
        # elif type_search == 'parent':
        #     SearchModel.objects.create(user=request.user, content_search=search_infor)
        #     return self.search_for_tutor(request, search_infor, q_object)
        # elif type_search == 'tutor':
        #     SearchModel.objects.create(user=request.user, content_search=search_infor)
        #     return self.search_for_parent(request, search_infor, q_object)

        if request.user.is_authenticated:
            SearchModel.objects.create(user=request.user, content_search=search_infor)

        if type_search == 'room':
            return self.search_for_room(request, search_infor, q_object)
        elif type_search == 'people':
            list_parent = self.search_parent(request, search_infor, q_object)
            list_tutor = self.search_tutor(request, search_infor, q_object)

            return Response({
                    'list_tutor': list_tutor,
                    'list_parent': list_parent
                })





