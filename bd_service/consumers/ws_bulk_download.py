import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from bd_service.views.data import get_progress_data_by_key


class BulkDownloadConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["id"]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        progress_data = get_progress_data_by_key(self.room_group_name)
        if progress_data is None:
            progress_data = 0
        else:
            progress_data = progress_data.decode('utf-8')

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notify_update_progress',
                'message': progress_data
            }
        )

    def notify_update_progress(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
