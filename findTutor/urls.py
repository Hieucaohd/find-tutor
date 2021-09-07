from django.urls import path, include
# from rest_framework.authtoken import views
from .viewsDic import (
                       tutorView, userAuthView, parentView, 
                       parentRoomView, priceView, waitingTutorView, 
                       customAuthToken, listInvitedView, tryTeachingView, 
                       tutorTeachingView, informationAboutRoomOfTutor, 
                       imagePrivateUserView, imageOfUserView, 
                      )

from graphene_django.views import GraphQLView
from .schema import schema

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # tutor
    path('tutorList/', tutorView.TutorList.as_view(), name='tutor-list'),
    path('tutorDetail/<int:pk>', tutorView.TutorDetail.as_view(), name='tutor-detail'),

    # parent
    path('parentList/', parentView.ParentList.as_view(), name='parent-list'),
    path('parentDetail/<int:pk>', parentView.ParentDetail.as_view(), name='parent-detail'),

    # parent room
    path('roomList/', parentRoomView.ParentRoomList.as_view(), name='room-list'),
    path('roomDetail/<int:pk>', parentRoomView.ParentRoomDetail.as_view(), name='room-detail'),

    # price
    path('priceList/', priceView.PriceList.as_view(), name='price-list'),
    path('priceDetail/<int:pk>', priceView.PriceDetail.as_view(), name='price-detail'),

    # waiting list
    path('waitingTutorList/', waitingTutorView.WaitingTutorList.as_view(), name='waiting-tutor-list'),
    path('waitingTutorDetail/<int:pk>', waitingTutorView.WaitingTutorDetail.as_view(), name='price-detail'),

    # invited list
    path('listInvitedList/', listInvitedView.ListInvitedList.as_view(), name='list-invited-list'),
    path('listInvitedDetail/<int:pk>', listInvitedView.ListInvitedDetail.as_view(), name='list-invited-detail'),

    # try teaching list
    path('tryTeachingList/', tryTeachingView.TryTeachingList.as_view(), name='try-teaching-list'),
    path('tryTeachingDetail/<int:pk>', tryTeachingView.TryTeachingDetail.as_view(), name='try-teaching-detail'),

    # teaching list
    path('teachingList/', tutorTeachingView.TutorTeachingList.as_view(), name='tutor-teaching-list'),
    path('teachingDetail/<int:pk>', tutorTeachingView.TutorTeachingDetail.as_view(), name='tutor-teaching-detail'),

    # information about room of tutor
    path('informationAboutRoomOfTutorList/', informationAboutRoomOfTutor.InforAboutRoomOfTutorList.as_view()),

    # for graphQL
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    # image private user
    path('imagePrivateUserList/', imagePrivateUserView.ImagePrivateUserList.as_view()),
    path('imagePrivateUserDetail/', imagePrivateUserView.ImagePrivateUserDetail.as_view()),

    # image of user
    path('imageOfUserList/', imageOfUserView.ImageOfUserList.as_view()),
    path('imageOfUserDetail/<int:pk>', imageOfUserView.ImageOfUserDetail.as_view()),
]