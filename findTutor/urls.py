from django.urls import path, include
from rest_framework.authtoken import views
from .viewsDic import tutorView, userAuthView, parentView, parentRoomView, priceView, waitingTutorView

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

    # price
    path('waitingTutorList/', waitingTutorView.WaitingTutorList.as_view(), name='waiting-tutor-list'),
    path('waitingTutorDetail/<int:pk>', waitingTutorView.WaitingTutorDetail.as_view(), name='price-detail'),

    # user
    path('userList/', userAuthView.UserList.as_view(), name='user-list'),
    path('userDetail/<int:pk>', userAuthView.UserDetail.as_view(), name='user-detail'),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
