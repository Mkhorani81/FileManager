from celery import Celery
from datetime import timedelta
import os
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FileManager.settings")

celery_app = Celery("FileManager")


celery_app.config_from_object("django.conf:settings", namespace="CELERY")


celery_app.autodiscover_tasks()


celery_app.conf.update(
    broker_url=config("CELERY_BROKER_URL", default="amqp://guest:guest@rabbitmq:5672//"),
    result_backend=config("CELERY_RESULT_BACKEND", default="rpc://"),
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=timedelta(days=1),
    task_always_eager=False,
    worker_prefetch_multiplier=4,
)
