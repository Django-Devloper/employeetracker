"""
url router for websocket connection
"""

from django.urls import path
from .consumers import AskGPTConsumer

websocket_patterns = [
    path("path/<str:group_name>/", AskGPTConsumer.as_asgi()),
]
