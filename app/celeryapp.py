from celery import Celery
from config import Config

celery = Celery('main', broker=Config.CELERY_BROKER_URL)


celery.autodiscover_tasks(['tasks'])