import asyncio
import logging
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.functional import cached_property
import websockets
logger = logging.getLogger(__name__)

AUTH_TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlIxMTc5NzMiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwiaWF0IjoxNjkxOTg5OTgwLCJleHAiOjE2OTIwNzYzODB9.upuvBzd7TcwVU72cAwKtyVZCnyBeMBPIKtEi_-CvQxrS1eUeehA-NheDZT3740kKB5xM7rjENxgLfvmUh8S2Cw"
API_KEY = "tSUk5UMV"
CLIENT_CODE = "R117973"
FEED_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlIxMTc5NzMiLCJpYXQiOjE2OTE5ODk5ODAsImV4cCI6MTY5MjA3NjM4MH0.cA-6KHi1WQQO1eNh6Xv8TolM7024xLTT8s-CoqnGwM40IJPgSvTIVE-YTqQjYj3ra6TBklvIVIzz-isKZ5C2mg"
correlation_id = "abc123"
action = 1
mode = 2
token_list = [
    {
        "exchangeType": 1,
        "tokens": ["2885"]
    }
]

class StockWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)

        # Accept the client connection. Use the subprotocol negotiated with the
        # target url.
        await self.accept(self.websocket.subprotocol)

        # Forward packets from the target websocket back to the client.
        self.consumer_task = asyncio.create_task(self.consume_from_target())


    async def disconnect(self, close_code):
        """The websocket consumer is shutting down. Shut down the connection to
        the target url."""

        # Disconnect can be called before self.consumer_task is created.

        if hasattr(self, 'consumer_task'):
            self.consumer_task.cancel()

            # Let the task complete
            await self.consumer_task

    async def receive(self, text_data=None, bytes_data=None):
        """Forward packets from the client to the target url."""

        try:
            await self.websocket.send(bytes_data or text_data)
        except websockets.ConnectionClosedError:
            # The target probably closed the connection.
            logger.exception('The outgoing connection was closed by the target.')
            await self.close()

    async def consume_from_target(self):
        """A websocket consumer to forward data from the target url to the client."""

        try:
            async for data in self.websocket:
                if hasattr(data, 'decode'):
                    await self.send(bytes_data=data)
                else:
                    await self.send(text_data=data)
        except asyncio.exceptions.CancelledError:
            # This is triggered by the consumer itself when the client connection is terminating.
            logger.debug('Shutting down the websocket consumer task and closing the outgoing websocket.')
            await self.websocket.close()
        except websockets.ConnectionClosedError:
            # The target probably closed the connection.
            logger.exception('The outgoing connection was closed by the target.')
            await self.close()