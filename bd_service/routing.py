from django.urls import re_path

from bd_service.consumers import ws_bulk_download

websocket_urlpatterns = [
    re_path(r'ws/bulk-download/(?P<id>\d+)/$',
            ws_bulk_download.BulkDownloadConsumer.as_asgi()),
]
