from django.urls import path
from .views import GoogleAuth

urlpatterns = [
    path("google-auth/", GoogleAuth.as_view(), name="google-authentication"),
]