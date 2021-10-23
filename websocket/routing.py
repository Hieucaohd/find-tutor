from django.urls import re_path

from notification.consumers import NotifyConsumer

websocket_urlpatterns = [
    re_path("ws/notification/", NotifyConsumer.as_asgi()),
]
