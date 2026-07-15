"""
ASGI config for conf project — Django Channels bilan yangilangan.
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # Oddiy HTTP so'rovlari Django'ga yo'naltiriladi
    'http': get_asgi_application(),

    # WebSocket so'rovlari Channels'ga yo'naltiriladi
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
