import logging
import random
from datetime import datetime

from django.http import HttpResponse
from redis import Redis
from rest_framework import status
from rest_framework.views import APIView
from rq import Queue
from rq import Retry

from bd_service.utils.response import error_response
from bd_service.utils.response import success_create_response
from bd_service.utils.response import success_get_all_response
from bd_service.views.data import delete_progress_and_download_data
from bd_service.views.data import get_download_data_by_key
from bd_service.views.data import get_multiple_download_and_progress_by_key
from bd_service.views.worker import download_videos

r = Redis(host='redis', port=6379)
q = Queue(connection=r)

logger = logging.getLogger(__name__)


class BulkDownloadView(APIView):
    def get(self, request):
        logger.info(f'[BulkDownload] GET request received: {datetime.now()}')

        bulk_download_id = request.query_params.get('bulkDownloadId')
        if bulk_download_id is None:
            return error_response('Parameter "bulkDownloadId" is required', status.HTTP_400_BAD_REQUEST)

        data = get_download_data_by_key(bulk_download_id)
        if data is None:
            return error_response(f'Data with id {bulk_download_id} cannot be found or still in progress', status.HTTP_404_NOT_FOUND)

        logger.info(f'[BulkDownload] GET request success: {datetime.now()}')
        delete_progress_and_download_data(bulk_download_id)
        return HttpResponse(data, content_type="application/zip")

    def post(self, request):
        logger.info(f'[BulkDownload] POST request received: {datetime.now()}')

        video_ids = request.data.get('videoIds')
        if video_ids is None:
            return error_response('Parameter "videoIds" is required', status.HTTP_400_BAD_REQUEST)

        key = str(random.randint(0, 1000)) + \
            str(int(round(datetime.now().timestamp())))
        q.enqueue(download_videos, args=(key, video_ids),
                  retry=Retry(max=3), timeout=3600, failure_ttl=86400)

        logger.info(f'[BulkDownload] POST request success: {datetime.now()}')
        return success_create_response(key)


class BulkDownloadAllView(APIView):
    def post(self, request):
        logger.info(
            f'[BulkDownloadAll] GET request received: {datetime.now()}')

        bulk_download_ids = request.data.get('bulkDownloadIds')
        if bulk_download_ids is None:
            return error_response('Parameter "bulkDownloadIds" is required', status.HTTP_400_BAD_REQUEST)

        download_data = get_multiple_download_and_progress_by_key(
            bulk_download_ids)

        logger.info(f'[BulkDownloadAll] GET request success: {datetime.now()}')
        return success_get_all_response(download_data)
