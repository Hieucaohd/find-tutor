"""
ASGI config for findTeacherProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

import notification.routing

from findTeacherProject.channel_token_auth import TokenAuthMiddlewareStack




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findTeacherProject.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            notification.routing.websocket_urlpatterns
        )
    ),
})
