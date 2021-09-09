# чтобы модуль celery.py выполнялся при старте проекта,
# его необходимо импортировать в данный файл
from .celery import app as celery_app

__all__ = ('celery_app',)