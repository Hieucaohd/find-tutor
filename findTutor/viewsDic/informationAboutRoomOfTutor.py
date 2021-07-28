from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from ..models import WaitingTutorModel, ListInvitedModel, TryTeachingModel, TutorTeachingModel, TutorModel


class InforAboutRoomOfTutorList(APIView):
    def get_tutor_from_request(self, request):
        try:
            return TutorModel.objects.get(user=request.user)
        except TutorModel.DoesNotExist as e:
            raise Http404

    def get(self, request, format=None):
        tutor = self.get_tutor_from_request(request)
        list_waiting = WaitingTutorModel.objects.filter(tutor=tutor)
        list_invited = ListInvitedModel.objects.filter(tutor=tutor)
        list_try_teaching = TryTeachingModel.objects.filter(tutor=tutor)
        list_teaching = TutorTeachingModel.objects.filter(tutor=tutor)

        list_room_waiting = []
        for waiting in list_waiting:
            list_room_waiting.append(waiting.parent_room.id)

        print(list_room_waiting)

        list_room_invited = []
        for invited in list_invited:
            list_room_invited.append(invited.parent_room.id)

        list_room_try_teaching = []
        for try_teaching in list_try_teaching:
            list_room_try_teaching.append(try_teaching.parent_room.id)

        list_room_teaching = []
        for teaching in list_teaching:
            list_room_teaching.append(teaching.parent_room.id)

        return Response({
            'list_room_waiting': list_room_waiting,
            'list_room_invited': list_room_invited,
            'list_room_try_teaching': list_room_try_teaching,
            'list_room_teaching': list_room_teaching,
        })