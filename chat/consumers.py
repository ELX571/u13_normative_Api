import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Umumiy chat Consumer.
    Barcha ulangan foydalanuvchilar 'general_chat' guruhiga qo'shiladi.
    """
    group_name = 'general_chat'

    async def connect(self):
        """Foydalanuvchi WebSocket orqali ulanadi."""
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        logger.info(f"[WS] Yangi ulanish: {self.channel_name}")

        # Barcha guruhdagilarga ulanish xabari
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': '🟢 Yangi foydalanuvchi chatga qo\'shildi!',
                'username': 'System',
            }
        )

    async def disconnect(self, close_code):
        """Foydalanuvchi uziladi."""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"[WS] Ulanish uzildi: {self.channel_name} | Kod: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        """Foydalanuvchidan xabar qabul qilinadi va guruhga tarqatiladi."""
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()
            username = data.get('username', 'Anonim').strip()

            if not message:
                return

            logger.info(f"[WS] Xabar: {username}: {message}")

            # Guruhning barcha a'zolariga xabar yuborish
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Noto\'g\'ri format'}))

    async def chat_message(self, event):
        """Guruhdan kelgan xabarni WebSocket orqali clientga yuboradi."""
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))
