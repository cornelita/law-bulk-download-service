import logging
import random
from datetime import datetime

import grpc
import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bd_service.utils.response import error_response
from bd_service.utils.response import success_post_response
from download_pb2 import VideoRequest
from download_pb2_grpc import DownloadServiceStub

logger = logging.getLogger(__name__)


class BulkDownloadView(APIView):
    download_data = {}

    def get(self, request):
        logger.info(f'[BulkDownload] GET request received: {datetime.now()}')

        bulk_download_id = request.query_params.get('bulkDownloadId')
        if bulk_download_id is None:
            return error_response('Parameter "bulkDownloadId" is required', status.HTTP_400_BAD_REQUEST)

        data = self.download_data.get(bulk_download_id)
        if data is None:
            return error_response(f'Data with id {bulk_download_id} cannot be found', status.HTTP_404_NOT_FOUND)

        logger.info(f'[BulkDownload] GET request success: {datetime.now()}')
        return HttpResponse(data)

    def post(self, request):
        logger.info(f'[BulkDownload] POST request received: {datetime.now()}')

        video_ids = request.data.get('videoIds')
        if video_ids is None:
            return error_response('Parameter "videoIds" is required', status.HTTP_400_BAD_REQUEST)

        key = str(random.randint(0, 1000)) + str(datetime.now().timestamp())
        self.download_videos(key, video_ids)

        logger.info(f'[BulkDownload] POST request success: {datetime.now()}')
        return success_post_response(key)

    def download_videos(self, key, video_ids):
        logger.info(f'[BulkDownload] Starting download video: {key}')
        paths = []
        try:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = DownloadServiceStub(channel)
                for video_id in video_ids:
                    response = stub.DownloadVideo(
                        VideoRequest(videoId=video_id))
                    paths.append(response.filePath)
                    logger.info(
                        f'[BulkDownload] Download video path received: {response.filePath}')
        except grpc.RpcError as e:
            logger.error(f'[BulkDownload] gRPC error raised: {e.details()}')
            return Response(data=f'Error raised: {e.details()}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.zip_file(key, paths)

    def zip_file(self, key, paths):
        logger.info(f'[BulkDownload] Starting zipping video: {key}')
        response = requests.post('http://localhost:8001/zipper/', json={
            'videos': paths
        })
        logger.info(f'[BulkDownload] Zip file received: {datetime.now()}')
        self.download_data[key] = response
