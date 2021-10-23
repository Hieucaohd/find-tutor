from django.urls import path, include

from notification.views import FollowRoomDetail, FollowRoomList, FollowUserDetail, FollowUserList

urlpatterns = [
    path("followRoomList/", FollowRoomList.as_view()),
    path("followRoomDetail/<int:room_id>", FollowRoomDetail.as_view()),
    path("followUserList/", FollowUserList.as_view()),
    path("followUserDetail/<int:user_id>", FollowUserDetail.as_view()),
]