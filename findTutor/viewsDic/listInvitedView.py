from ..models import ListInvitedModel, TutorModel, TryTeachingModel, ParentRoomModel
from ..serializers import ListInvitedSerializer, TryTeachingSerializer

from .baseView import ListCreateBaseView, RetrieveUpdateDeleteBaseView

from rest_framework import permissions, status
from rest_framework.response import Response

from findTutor.signals import tutor_out_room

from django.http import Http404


class ListInvitedList(ListCreateBaseView):
    """
        Just tutor can see the list of Invited him/her.
    """
    permission_classes = [permissions.IsAuthenticated]

    modelBase = ListInvitedModel
    serializerBase = ListInvitedSerializer

    def get_pk_room(self, request):
        try:
            return int(request.query_params['pk_room'])
        except Exception as e:
            return False

    def get_room(self, request):
        pk_room = self.get_pk_room(request)
        try:
            return ParentRoomModel.objects.get(pk=pk_room)
        except ParentRoomModel.DoesNotExist as e:
            raise Http404

    def get_tutor_from_request(self, request):
        try:
            return TutorModel.objects.get(user=request.user)
        except TutorModel.DoesNotExist as e:
            raise Http404

    def get_for_tutor(self, request, format=None):
        """
            Return invited room for tutor from request when login.
        """
        tutor = self.get_tutor_from_request(request)
        list_invited = self.modelBase.objects.filter(tutor=tutor)
        serializer = self.serializerBase(list_invited, many=True)
        return Response(serializer.data)

    def get_for_room(self, request, format=None):
        """
            Return invited tutor for a room.
        """
        parent_room = self.get_room(request)
        list_invited = self.modelBase.objects.filter(parent_room=parent_room)
        serializer = self.serializerBase(list_invited, many=True)
        return Response(serializer.data)

    def get(self, request, format=None):
        if self.get_pk_room(request):
            return self.get_for_room(request)
        else:
            return self.get_for_tutor(request)

    def post(self, request, format=None):
        return Response(status=status.HTTP_403_FORBIDDEN)


class ListInvitedDetail(RetrieveUpdateDeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = ListInvitedModel
    serializerBase = ListInvitedSerializer

    def get_tutor_from_request(self, request):
        try:
            return TutorModel.objects.get(user=request.user)
        except TutorModel.DoesNotExist as e:
            raise Http404

    def isTutorBeInvited(self, request, pk):
        invite = self.get_object(pk)
        tutor = self.get_tutor_from_request(request)
        return invite.tutor == tutor

    def isRoomHasTutorTryTeaching(self, request, pk):
        parent_room = self.get_object(pk).parent_room
        try_teaching = TryTeachingModel.objects.filter(parent_room=parent_room)
        if try_teaching:
            return True
        return False

    def isParentInvited(self, request, pk):
        item = self.get_object(pk)
        return item.parent_room.parent.user == request.user

    def put(self, request, pk, format=None):
        """
            This is called when tutor agree to try teaching.
        """
        if self.isTutorBeInvited(request, pk):
            invited = self.get_object(pk)
            serializer = self.serializerBase(invited, data=request.data)
            if serializer.is_valid():

                # take tutor and room to Try Teaching.
                if not self.isRoomHasTutorTryTeaching(request, pk):
                    # serializer.save(tutor_agree=True)
                    
                    tutor = self.get_tutor_from_request(request)
                    parent_room = invited.parent_room
                    new_try_teaching = TryTeachingModel.objects.create(tutor=tutor, parent_room=parent_room)
                    data = TryTeachingSerializer(new_try_teaching, many=False).data
                    print(data)
                    invited.delete()
                    # notification for parent that tutor agree to try teaching.
                    
                else:
                    # notification for tutor that: room is having a another tutor try teaching.

                    return Response(status=status.HTTP_403_FORBIDDEN)

                return Response(data)
            return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        """
            This is called when tutor not agree to try teaching or parent don't want tutor in list_invited any more.
        """
        invited_item = self.get_object(pk)
        if self.isTutorBeInvited(request, pk):
            # notification for parent that tutor don't agree to try teaching.
            threading.Thread(target=tutor_out_room.send, kwargs={"user_send": request.user,
                                                                  "user_receive": invited_item.parent_room.parent.user,
                                                                  "content": f"Gia sư {request.user.tutormodel.full_name} không đồng ý dạy lớp {invited_item.parent_room.subject} {invited_item.parent_room.lop} của bạn",
                                                                  "instance": invited_item,
                                                                  "sender": self.__class__}).start()

            return super().delete(request, pk)
        elif self.isParentInvited(request, pk):
            # notification for tutor that parent don't want him/her to try teaching any more.
            threading.Thread(target=tutor_out_room.send, kwargs={"user_send": request.user,
                                                                  "user_receive": invited_item.tutor.user,
                                                                  "content": f"Phụ huynh {request.user.parentmodel.full_name} không muốn tiếp tục mời bạn dạy lớp {invited_item.parent_room.subject} {invited_item.parent_room.lop} của họ",
                                                                  "instance": invited_item,
                                                                  "sender": self.__class__}).start()

            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
