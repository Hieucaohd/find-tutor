from django.urls import path
from .views import *


urlpatterns = [
	# tutor
	path('tutorList/', CommentAboutTutorList.as_view(), name='comment-tutor-list'),
	path('tutorDetail/', CommentAboutTutorDetail.as_view(), name='comment-tutor-detail'),

	# parent
	path('parentList/', CommentAboutParentList.as_view(), name='comment-parent-list'),
	path('parentDetail/', CommentAboutParentDetail.as_view(), name='comment-parent-detail'),

	# parent room
	path('parent-roomList/', CommentAboutParentRoomList.as_view(), name='comment-parent-room-list'),
	path('parent-roomDetail/', CommentAboutParentRoomDetail.as_view(), name='comment-parent-room-detail'),
]