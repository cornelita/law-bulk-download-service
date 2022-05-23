from rest_framework import status
from rest_framework.response import Response


def success_create_response(bulkDownloadId):
    return Response(
        data={
            'bulkDownloadId': bulkDownloadId,
        },
        status=status.HTTP_200_OK,
    )


def success_get_all_response(data):
    return Response(
        data={
            'data': data,
        },
        status=status.HTTP_200_OK,
    )


def error_response(message, response_status=status.HTTP_500_INTERNAL_SERVER_ERROR):
    return Response(
        data={
            'detail': message,
        },
        status=response_status,
    )
