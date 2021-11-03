from django.urls import path
from .views import (RegisterHttpOnlyCookie, 
                    VerifyEmail, 
                    LoginHttpOnlyCookie, 
                    Logout, 
                    GetInforByToken, 
                    ChangePassword,
                    LinkDetail,
                    MultipleLinkDetail,)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterHttpOnlyCookie.as_view(), name='register'),
    path('login/', LoginHttpOnlyCookie.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('getInforByToken/', GetInforByToken.as_view()),
    path('changePassword/', ChangePassword.as_view()),
    path('linkDetail/<int:pk>', LinkDetail.as_view()),
    path('updateMultipleLink/', MultipleLinkDetail.as_view()),
]