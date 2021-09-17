from findTutor.checkTutorAndParent import isTutor
from .views import SearchShow
from django.db.models import Q
search_instance = SearchShow()

class ResolveSearch:
    def __init__(self, model, fields, kwargs):
        self.model = model
        self.fields = fields
        self.kwargs = kwargs

        self.list_query = []

        self.get_location_query()

    def get_location_query(self):
        province_code = self.kwargs.get('province_code')
        district_code = self.kwargs.get('district_code')
        ward_code = self.kwargs.get('ward_code')

        if ward_code:
            self.list_query.append(Q(ward_code=ward_code))
        elif district_code:
            self.list_query.append(Q(district_code=district_code))
        elif province_code:
            self.list_query.append(Q(province_code=province_code))

    def resolve_search(self):

        search_infor = self.kwargs.get('search_infor')

        if search_infor:
            search_infor = search_instance.normal_search_infor(search_infor)
            return search_instance.search_engine(model=self.model, 
                                                 list_query=self.list_query, 
                                                 search_infor=search_infor, 
                                                 fields=self.fields)
        else:
            return search_instance.search_with_no_search_infor(model=self.model, 
                                                               list_query=self.list_query)


class ResolveSearchForRoom(ResolveSearch):

    def __init__(self, model, fields, kwargs):
        # call super init
        ResolveSearch.__init__(self, model=model, fields=fields, kwargs=kwargs)

        self.get_price_query()
        self.get_type_teacher_query()
        self.get_sex_of_teacher_query()
        self.get_lop_query()
        self.get_suitable_room_query()

    def string_is_number(self, string_number):
        try:
            string_number = int(string_number)
            return True
        except ValueError:
            return False

    def tach_lop(self, search_infor):
        last_index = len(search_infor) - 1
        b = search_infor.find('lop')    # b

        if last_index >= b+5:
            word_b4 = search_infor[b+4]
            word_b5 = search_infor[b+5]

            if self.string_is_number(word_b5) and self.string_is_number(word_b4):
                return int(word_b4+word_b5)
            elif self.string_is_number(word_b4):
                return int(word_b4)
            else:
                return None
        elif last_index == b+4:
            word_b4 = search_infor[b+4]
            if self.string_is_number(word_b4):
                return int(word_b4)
            else:
                return None
        else:
            return None

    def normal_search_infor(self, search_infor):
        search_infor = search_instance.normal_search_infor(search_infor)

        replace_what = [{'word_replace': 'mon ', 'with': ''}, 
                        {'word_replace': ' hoc', 'with': ''}]

        for item in replace_what:
            search_infor = search_infor.replace(item.get('word_replace'), item.get('with'))


        if 'lop' in search_infor:
            number_lop = self.tach_lop(search_infor)

            if number_lop:
                lop_from_kwargs = self.kwargs.get('lop')
                if lop_from_kwargs:
                    lop_from_kwargs.append(number_lop)
                    self.get_lop_query()
                else:
                    self.kwargs['lop'] = [number_lop]
                    self.get_lop_query()

                search_infor = search_infor.replace(' ' + str(number_lop), '', 1)

            b = search_infor.find('lop')
            if b == 0:
                search_infor = search_infor.replace('lop', '', 1)
            else:
                search_infor = search_infor.replace(' lop', '', 1)

        return search_infor

    def get_price_query(self):
        price = self.kwargs.get('price')
        if price and len(price) >= 2:
            min_price = min(price)
            max_price = max(price)

            self.list_query.append(Q(pricemodel__money_per_day__gte=min_price) & Q(pricemodel__money_per_day__lte=max_price))

    def get_type_teacher_query(self):
        type_teachers = self.kwargs.get('type_teacher')
        type_teacher_query = Q()
        if type_teachers:
            for type_teacher in type_teachers:
                type_teacher_query &= Q(pricemodel__type_teacher__icontains=type_teacher)
            self.list_query.append(type_teacher_query)


    def get_sex_of_teacher_query(self):
        sex_of_teacher = self.kwargs.get('sex_of_teacher')
        if sex_of_teacher:
            self.list_query.append(Q(pricemodel__sex_of_teacher__icontains=sex_of_teacher))

    def get_lop_query(self):
        lops = self.kwargs.get("lop")
        lop_query = Q()
        if lops:
            for lop in lops:
                lop_query |= Q(lop=lop)
            self.list_query.append(lop_query)

    def get_suitable_room_query(self):
        request = kwargs.get('request')
        if request.user.is_authenticated and isTutor(request.user):
            user_not_in_list = (~Q(waitingtutormodel__tutor__user=request.user) & 
                                ~Q(listinvitedmodel__tutor__user=request.user) &
                                ~Q(tryteachingmodel__tutor__user=request.user) &
                                ~Q(tutorteachingmodel__tutor__user=request.user)
                                )
            self.list_query.append(user_not_in_list)

    def resolve_search(self):

        search_infor = self.kwargs.get('search_infor')
        if search_infor:
            search_infor = self.normal_search_infor(search_infor)

        if search_infor:
            return search_instance.search_engine(model=self.model, 
                                                 list_query=self.list_query, 
                                                 search_infor=search_infor, 
                                                 fields=self.fields)
        else:
            return search_instance.search_with_no_search_infor(model=self.model, list_query=self.list_query)


class ResolveSearchForTutor(ResolveSearch):
    def __init__(self, model, fields, kwargs):
        # call parent init
        ResolveSearch.__init__(self, model=model, fields=fields, kwargs=kwargs)

        self.get_lop_query()

    def get_lop_query(self):
        lops = self.kwargs.get("lop")
        lop_query = Q()
        if lops:
            for lop in lops:
                lop_query |= Q(lop_day__icontains=str(lop))
            self.list_query.append(lop_query)


class ResolveSearchForParent(ResolveSearch):
    pass
