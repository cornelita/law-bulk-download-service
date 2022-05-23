import logging
from datetime import datetime

import grpc
import requests
from rest_framework import status
from rest_framework.response import Response

from bd_service.constants import K_API_DOWNLOAD_URL
from bd_service.constants import K_API_ZIPPER_URL
from bd_service.views.data import set_download_data
from bd_service.views.data import set_progress_data
from download_pb2 import VideoRequest
from download_pb2_grpc import DownloadServiceStub

logger = logging.getLogger(__name__)


def download_videos(key, video_ids):
    logger.info(f'[BulkDownload] Starting download video: {key}')
    paths = []
    # 100 / (total video + zipping result)
    progress_calc = 100 / (len(video_ids) + 1)
    progress_job = 0
    try:
        with grpc.insecure_channel(K_API_DOWNLOAD_URL) as channel:
            stub = DownloadServiceStub(channel)
            for video_id in video_ids:
                response = stub.DownloadVideo(
                    VideoRequest(videoId=video_id))
                paths.append(response.filePath)
                logger.info(
                    f'[BulkDownload] Download video path received: {response.filePath}')
                progress_job += progress_calc
                set_progress_data(key, progress_job)
    except grpc.RpcError as e:
        logger.error(f'[BulkDownload] gRPC error raised: {e.details()}')
        set_progress_data(key, -1)  # error
        set_download_data(key, Response(
            data=f'Error raised: {e.details()}', status=status.HTTP_500_INTERNAL_SERVER_ERROR))
        return

    zip_file(key, paths)


def zip_file(key, paths):
    logger.info(f'[BulkDownload] Starting zipping video: {key}')
    response = requests.post(f'{K_API_ZIPPER_URL}/zipper/', json={
        'videos': paths
    })
    if response.status_code != 200:
        set_progress_data(key, -1)
        raise RuntimeError('Zip failed')
    else:
        logger.info(f'[BulkDownload] Zip file received: {datetime.now()}')
        set_download_data(key, response.content)
        set_progress_data(key, 100)
