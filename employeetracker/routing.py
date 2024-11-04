"""
url router for websocket connection
"""

from django.urls import path
from .consumers import AskGPT

websocket_patterns = [
    path("path/<str:group_name>/", AskGPT.as_asgi()),
]
