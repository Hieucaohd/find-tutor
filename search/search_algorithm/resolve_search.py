from findTutor.checkTutorAndParent import isTutor

from django.db.models import Q

from .search import FullTextSearch, FuzzySearch

from abc import abstractproperty, abstractmethod

from typing import Sequence


class ResolveSearch:
    search_instance = None

    def __init__(self, model, fields, kwargs):
        self.model = model
        self.fields = fields
        self.kwargs = kwargs
        self.list_querys = []

        self._get_location_query()

    def _get_location_query(self):
        province_code = self.kwargs.get('province_code')
        district_code = self.kwargs.get('district_code')
        ward_code = self.kwargs.get('ward_code')

        if ward_code:
            self.list_querys.append(Q(ward_code=ward_code))
        elif district_code:
            self.list_querys.append(Q(district_code=district_code))
        elif province_code:
            self.list_querys.append(Q(province_code=province_code))

    def resolve_search(self) -> Sequence:
        search_infor = self.kwargs.get("search_infor")

        search_result = self.search_instance(model=self.model,
                                      search_text=search_infor,
                                      list_fields=self.fields,
                                      list_querys=self.list_querys).get_result()

        return search_result


class ResolveSearchForRoom(ResolveSearch):
    search_instance = FullTextSearch

    def __init__(self, model, fields, kwargs):
        # call super init
        ResolveSearch.__init__(self, model=model, fields=fields, kwargs=kwargs)

        self.list_querys.append(Q(tutorteachingmodel = None))

        self._get_price_query()
        self._get_type_teacher_query()
        self._get_sex_of_teacher_query()
        self._get_lop_query()
        self._get_suitable_room_query()

    def _get_price_query(self) -> None:
        price = self.kwargs.get('price')
        if price and len(price) >= 2:
            min_price = min(price)
            max_price = max(price)

            self.list_querys.append(Q(pricemodel__money_per_day__gte=min_price) & Q(pricemodel__money_per_day__lte=max_price))

    def _get_type_teacher_query(self) -> None:
        type_teachers = self.kwargs.get('type_teacher')
        type_teacher_query = Q()
        if type_teachers:
            for type_teacher in type_teachers:
                type_teacher_query &= Q(pricemodel__type_teacher__icontains=type_teacher)
            self.list_querys.append(type_teacher_query)


    def _get_sex_of_teacher_query(self) -> None:
        sex_of_teacher = self.kwargs.get('sex_of_teacher')
        if sex_of_teacher:
            self.list_querys.append(Q(pricemodel__sex_of_teacher__icontains=sex_of_teacher))

    def _get_lop_query(self) -> None:
        lops = self.kwargs.get("lop")
        lop_query = Q()
        if lops:
            for lop in lops:
                lop_query |= Q(lop=lop)
            self.list_querys.append(lop_query)

    def _get_suitable_room_query(self) -> None:
        request = self.kwargs.get('request')
        if request.user.is_authenticated and isTutor(request.user):
            user_not_in_list = (~Q(waitingtutormodel__tutor__user=request.user) & 
                                ~Q(listinvitedmodel__tutor__user=request.user) &
                                ~Q(tryteachingmodel__tutor__user=request.user) &
                                ~Q(tutorteachingmodel__tutor__user=request.user)
                                )
            self.list_querys.append(user_not_in_list)

    def resolve_search(self) -> Sequence:
        search_infor = self.kwargs.get('search_infor')
        order_by = self.kwargs.get('order_by')

        order_list = {
            "create_at": "-create_at",     
            "price_asc": "pricemodel",
            "price_desc": "-pricemodel",
        }

        full_text_search = self.search_instance(model=self.model,
                                      search_text=search_infor,
                                      list_fields=self.fields,
                                      list_querys=self.list_querys)
        get_order = order_list.get(order_by, "create_at")
        result = full_text_search.get_result().order_by(get_order)

        return result


class ResolveSearchForTutor(ResolveSearch):
    search_instance = FuzzySearch

    def __init__(self, model, fields, kwargs) -> None:
        # call parent init
        ResolveSearch.__init__(self, model=model, fields=fields, kwargs=kwargs)

        self._get_lop_query()

    def _get_lop_query(self) -> None:
        lops = self.kwargs.get("lop")
        lop_query = Q()
        if lops:
            for lop in lops:
                lop_query |= Q(lop_day__icontains=str(lop))
            self.list_querys.append(lop_query)


class ResolveSearchForParent(ResolveSearch):
    search_instance = FuzzySearch
