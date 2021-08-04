from django.urls import path
from .views import Search


urlpatterns = [
	# search
    path('', Search.as_view(), name='search'),
]