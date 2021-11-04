import os
from django.conf.urls import url
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findTeacherProject.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import websocket.routing
import findTutor.routing

from authentication.custom_jwt_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            websocket.routing.websocket_urlpatterns +
            findTutor.routing.websocket_urlpatterns   
        )
    ),
})
