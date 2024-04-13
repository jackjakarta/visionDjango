from celery import shared_task
from django.core.cache import cache


@shared_task(bind=True)
def process_data(self, data):
    # Process data by converting it to uppercase
    result = data.upper()
    # Use Celery's built-in request ID as the job ID
    job_id = self.request.id
    # Store result in cache with a timeout of 1 hour
    cache.set(job_id, result, timeout=3600)
    return job_id


@shared_task
def task_one():
    return "It works!"
