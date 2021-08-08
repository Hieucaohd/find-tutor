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

        result_1 = fuzz.ratio(source, have)
        result_1_1 = fuzz.ratio(self.normal_search_infor(source), self.normal_search_infor(have))

        result_2 = fuzz.partial_ratio(source, have)
        result_2_2 = fuzz.partial_ratio(self.normal_search_infor(source), self.normal_search_infor(have))

        result_3 = pylcs.lcs2(self.normal_search_infor(source), self.normal_search_infor(have)) / len(source) * 100
        result_3_3 = pylcs.lcs(self.normal_search_infor(source), self.normal_search_infor(have)) / len(source) * 100

        score = max(result_1, result_1_1, result_2, result_2_2, result_3, result_3_3)
        print(score)

        limit = 75

        return (result_1 >= limit) or \
               (result_1_1 >= limit) or \
               (result_2 >= limit) or \
               (result_2_2 >= limit) or \
               (result_3 >= limit) or \
               (result_3_3 >= limit)

    def search_for_tutor(self, request, search_infor, q_object):
        list_parent = (parent for parent in ParentModel.objects.filter(q_object) if
                       self.test_for_string(parent.full_name, search_infor))

        data_parent = ParentSerializer(list_parent, many=True)

        return Response(data_parent.data)

    def search_for_parent(self, request, search_infor, q_object):
        list_tutor = (tutor for tutor in TutorModel.objects.filter(q_object) if
                      self.test_for_string(tutor.full_name, search_infor) or
                      self.test_for_string(tutor.experience, search_infor) or
                      self.test_for_string(tutor.achievement, search_infor) or 
                      self.test_for_string(tutor.university, search_infor))

        data_tutor = TutorSerializer(list_tutor, many=True)

        return Response(data_tutor.data)

    def search_for_room(self, request, search_infor, q_object):
        list_parent_room = (room for room in ParentRoomModel.objects.filter(q_object) if
                            self.test_for_string(room.subject, search_infor) or
                            self.test_for_string(room.other_require, search_infor))

        data_parent_room = ParentRoomSerializer(list_parent_room, many=True)

        return Response(data_parent_room.data)

    def get(self, request, format=None):
        province_code = request.query_params.get('province_code', 0)
        if not province_code:
            province_code = 0

        district_code = request.query_params.get('district_code', 0)
        if not district_code:
            district_code = 0

        ward_code = request.query_params.get('ward_code', 0)
        if not ward_code:
            ward_code = 0

        room = request.query_params.get('room', 0)

        search_infor = request.query_params.get('search', '')
        search_infor = self.normal_search_infor(search_infor)

        q_object = Q(province_code = int(province_code)) | Q(district_code = int(district_code)) | Q(ward_code = int(ward_code))
        

        if room:
            return self.search_for_room(request, search_infor, q_object)
        elif isTutor(request.user):
            SearchModel.objects.create(user=request.user, content_search=search_infor)
            return self.search_for_tutor(request, search_infor, q_object)
        elif isParent(request.user):
            SearchModel.objects.create(user=request.user, content_search=search_infor)
            return self.search_for_parent(request, search_infor, q_object)
        



