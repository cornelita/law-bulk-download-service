import logging

import grpc
import requests
from redis import Redis
from rest_framework import status
from rest_framework.response import Response

from bd_service.constants import K_API_DOWNLOAD_URL
from bd_service.constants import K_API_ZIPPER_URL
from bd_service.views.data import set_download_data
from bd_service.views.data import set_progress_data
from download_pb2 import VideoRequest
from download_pb2_grpc import DownloadServiceStub

logger = logging.getLogger(__name__)


r = Redis(host='redis', port=6379)


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
                r.publish(key, key)
    except grpc.RpcError as e:
        logger.error(f'[BulkDownload] gRPC error raised: {e.details()}')
        set_progress_data(key, -1)  # error
        r.publish(key, key)
        set_download_data(key, Response(
            data=f'Error raised: {e.details()}', status=status.HTTP_500_INTERNAL_SERVER_ERROR))
        return

    try:
        content = zip_file(key, paths)
        set_download_data(key, content)
        set_progress_data(key, 100)
        r.publish(key, key)
    except (AssertionError, ConnectionError) as e:
        logger.error(f'[BulkDownload] Error raised: {e}')
        set_progress_data(key, -1)  # error
        r.publish(key, key)
        raise


def zip_file(key, paths):
    logger.info(f'[BulkDownload] Starting zipping video: {key}')
    response = requests.post(f'{K_API_ZIPPER_URL}/zipper/', json={
        'videos': paths
    })
    assert(response.status_code == 200)
    return response.content
