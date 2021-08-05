from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from findTutor.serializers import TutorSerializer, ParentSerializer, ParentRoomSerializer
from findTutor.models import TutorModel, ParentModel, ParentRoomModel
from findTutor.checkTutorAndParent import isTutor, isParent

from .models import SearchModel


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

        limit = 70

        return (result_1 >= limit) or \
               (result_1_1 >= limit) or \
               (result_2 >= limit) or \
               (result_2_2 >= limit) or \
               (result_3 >= limit) or \
               (result_3_3 >= limit)

    def search_for_tutor(self, request, search_infor):
        list_parent_room = (room for room in ParentRoomModel.objects.all() if
                            self.test_for_string(room.subject, search_infor) or
                            self.test_for_string(room.other_require, search_infor))

        list_parent = (parent for parent in ParentModel.objects.all() if
                       self.test_for_string(parent.getFullName(), search_infor))

        data_parent_room = ParentRoomSerializer(list_parent_room, many=True)
        data_parent = ParentSerializer(list_parent, many=True)

        return Response({
            'data_parent_room': data_parent_room.data,
            'data_parent': data_parent.data,
        })

    def search_for_parent(self, request, search_infor):
        list_tutor = (tutor for tutor in TutorModel.objects.all() if
                      self.test_for_string(tutor.getFullName(), search_infor) or
                      self.test_for_string(tutor.experience, search_infor) or
                      self.test_for_string(tutor.achievement, search_infor) or 
                      self.test_for_string(tutor.university, search_infor))

        data_tutor = TutorSerializer(list_tutor, many=True)

        return Response({
            'data_tutor': data_tutor.data
        })

    def get(self, request, format=None):
        province_code = request.query_params.get('province_code', 0)
        district_code = request.query_params.get('district_code', 0)
        ward_code = request.query_params.get('ward_code', 0)

        search_infor = request.query_params.get('search', '')
        # print(search_infor)
        search_infor = self.normal_search_infor(search_infor)
        # print(search_infor)

        SearchModel.objects.create(user=request.user, content_search=search_infor)

        if isTutor(request.user):
            return self.search_for_tutor(request, search_infor)

        if isParent(request.user):
            return self.search_for_parent(request, search_infor)




        


