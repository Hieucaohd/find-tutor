from django.urls import path
from .views import GoogleAuth, FacebookAuth

urlpatterns = [
    path("google-auth/", GoogleAuth.as_view(), name="google-authentication"),
    path("facebook-auth/", FacebookAuth.as_view(), name="facebook-authentication"),
]