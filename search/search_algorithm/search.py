from django.db.models import Q
from django.db import models
from django.contrib.postgres.search import SearchVector

from findTutor.models import TutorModel, ParentModel, ParentRoomModel

from .utils import compare_two_string, replace_special_character

from abc import ABCMeta, abstractmethod

from typing import List, Union, Sequence


class Search(metaclass=ABCMeta):

    def __init__(self, model: models, 
                       search_text: str, 
                       list_fields: List[str], 
                       list_querys: List[Q]) -> None:
        self._model = model                 # la model client dang muon tim kiem tren do
        self._search_text = search_text     # la doan text tim kiem 
        self._list_fields = list_fields     # la nhung field can tim kiem boi _search_text.
        self._list_querys = list_querys     # la kieu kien loc.

    def _get_query_set(self):
        """
            day la bo loc co gia tri co dinh.
            co gang khien cho ket qua loc co so luong thap nhat.
        """

        sum_query = Q()
        for query in self._list_querys:
            sum_query &= query
        return self._model.objects.filter(sum_query)
    
    @abstractmethod
    def get_result(self) -> Sequence: pass


class FuzzySearch(Search):
    
    @staticmethod
    def __compare_search_text(search_text: str,
                              field_values: List[str]) -> int:
        """
            so sanh _search_text voi tung field trong record, moi field se 
            co mot so diem tuong ung (so sanh su giong nhau giua 2 chuoi). 
            Lay diem cao nhat. 
        """

        max_result = max(compare_two_string(search_text, replace_special_character(field)) 
                                            for field in field_values if field)
        return max_result

    def _sorted_fuzzy_search_result(self) -> Sequence[Union[ParentRoomModel, ParentModel, TutorModel]]:

        """
            so sanh _search_text voi tung record trong table, moi record 
            se co mot so diem tuong ung khi so sanh voi _search_text.
        """

        query_set = self._get_query_set()
    
        field_values = lambda record: [ getattr(record, field, '') for field in self._list_fields ]
        
        list_results = list( {
                                'record':record, 
                                'score': self.__compare_search_text(self._search_text, 
                                                                    field_values(record)),
                            } 
                            for record in query_set
                        )

        # sap xep ket qua tim kiem tu cao toi thap
        get_score = lambda result: result.get("score", 0)
        list_results.sort(key=get_score, reverse=True)

        # lay ket qua
        list_records = [result.get("record") for result in list_results if result.get("score") >= 50]
        return list_records

    def get_result(self) -> Sequence:
        self._search_text = replace_special_character(self._search_text)

        if self._search_text == None or self._search_text == '':
            return self._get_query_set()

        return self._sorted_fuzzy_search_result()


class FullTextSearch(Search):

    def get_result(self) -> Sequence:
        query_set = self._get_query_set()

        if self._search_text != '' and self._search_text != None:
            query_set = query_set.annotate(
                    search=SearchVector(*self._list_fields),
                    ).filter(search=self._search_text)

        return query_set




