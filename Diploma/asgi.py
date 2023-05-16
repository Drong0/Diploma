import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import chat.routing
from django.conf import settings
settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Diploma.settings")
django_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_app, # Use the separate Django application for HTTP requests
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)