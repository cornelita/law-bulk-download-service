from threading import Thread

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from redis import Redis

from bd_service.views.data import get_progress_data_by_key

r = Redis(host='redis', port=6379)


class Listener(Thread):
    def __init__(self, r, channels):
        Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        self.notify_update_progress(item['channel'])

    def run(self):
        for item in self.pubsub.listen():
            self.work(item)

    def notify_update_progress(self, bulk_download_id):
        channel_layer = get_channel_layer()
        progress_data = get_progress_data_by_key(bulk_download_id)
        async_to_sync(channel_layer.group_send)(
            bulk_download_id,
            {
                'type': 'notify_update_progress',
                'message': progress_data
            }
        )
