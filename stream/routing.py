from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/stock/', consumers.StockWebsocketConsumer.as_asgi()),
]