from celery import Celery

from app.config import Config

celery = Celery(
    'main', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_BACKEND_URL
)

celery.conf.task_track_started = True
celery.conf.task_serializer = 'json'
celery.conf.result_serializer = 'json'
celery.conf.accept_content = ['json']
celery.conf.event_serializer = 'json'
# celery.conf.result_expires=200
celery.conf.result_persistent = True
celery.conf.worker_send_task_events = False
celery.conf.worker_prefetch_multiplier = 1

celery.autodiscover_tasks(['app.tasks.database', 'app.tasks.product'])
