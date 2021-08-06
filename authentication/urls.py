from django.urls import path
from .views import RegisterView, VerifyEmail, Login, Logout

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]