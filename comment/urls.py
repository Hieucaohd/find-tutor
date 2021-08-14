from django.urls import path
from .views import *


urlpatterns = [
	# # tutor
	# path('tutorList/', CommentAboutTutorList.as_view(), name='comment-tutor-list'),
	# path('tutorDetail/', CommentAboutTutorDetail.as_view(), name='comment-tutor-detail'),

	# # parent
	# path('parentList/', CommentAboutParentList.as_view(), name='comment-parent-list'),
	# path('parentDetail/', CommentAboutParentDetail.as_view(), name='comment-parent-detail'),

	# user
	path('userList/', CommentAboutUserList.as_view(), name='comment-user-list'),
	path('userDetail/', CommentAboutUserDetail.as_view(), name='comment-user-detail'),

	# parent room
	path('parentRoomList/', CommentAboutParentRoomList.as_view(), name='comment-parent-room-list'),
	path('parentRoomDetail/', CommentAboutParentRoomDetail.as_view(), name='comment-parent-room-detail'),
]