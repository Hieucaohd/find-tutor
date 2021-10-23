from django.urls import re_path

from websocket.consumers import NotifyConsumer

websocket_urlpatterns = [
    re_path("ws/websocket/", NotifyConsumer.as_asgi()),
]
