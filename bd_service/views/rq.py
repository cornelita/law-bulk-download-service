from redis import Redis
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rq import Queue

connection = Redis(host='redis', port=6379)
queue = Queue(connection=connection)
registry = queue.failed_job_registry


@api_view(['GET'])
def requeue_jobs(request):
    job_ids = []
    try:
        # This is how to get jobs from FailedJobRegistry
        for job_id in registry.get_job_ids():
            registry.requeue(job_id)  # Puts job back in its original queue
            job_ids.append(job_id)
    except Exception:
        return Response('Failed!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(f'OK! {job_ids}')
