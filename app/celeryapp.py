from celery import Celery

from app.config import Config

celery = Celery(
    'main', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_BACKEND_URL
)

celery.conf.update(task_track_started=True)
celery.conf.update(task_serializer='pickle')
celery.conf.update(result_serializer='pickle')
celery.conf.update(accept_content=['pickle', 'json'])
celery.conf.update(result_expires=200)
celery.conf.update(result_persistent=True)
celery.conf.update(worker_send_task_events=False)
celery.conf.update(worker_prefetch_multiplier=1)

celery.autodiscover_tasks(['app.tasks.database', 'app.tasks.product'])
