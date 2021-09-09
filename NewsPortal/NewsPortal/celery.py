# импортируем библиотеку для взаимодействия с операционной системой
import os
# импортируем библиотеку Celery
from celery import Celery
from celery.schedules import crontab

# Задаём переменную окружения DJANGO_SETTINGS_MODULE для консольных команд Celery
# укажем файл настроек нашего проекта NewsPortal.settings
# так мы связываем настройки Django с настройками Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

# создаем экземпляр приложения 'NewsPortal' через наследование
app = Celery('NewsPortal')

# с помощью config_from_object загружаем конфигурацию из настроек нашего проекта
# параметр namespace определяет префикс, который мы будем добавлять для всех настроек, связанных с Celery,
# чтобы Celery сам находил все необходимые настройки в общем конфигурационном файле settings.py.
# Таким образом, в файле settings.py можно будет задавать конфигурацию Celery через настройки вида CELERY_,
# например CELERY_BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# вызовем процесс поиска и загрузки асинхронных задач по нашему проекту.
# Celery пройдет по всем приложениям, указанным в настройке INSTALLED_APPS,
# и попытается найти файл tasks.py, чтобы загрузить код задач.
app.autodiscover_tasks()


app.conf.beat_schedule = {

    'action_every_monday_8am': {
        'task': 'NewsPaper.newsletter.tasks.week_post',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),

    },
}

# app.conf.beat_schedule = {
#     'add-every-1-seconds': {
#         'task': 'NewsPaper.newsletter.tasks.week_post',
#         'schedule': 1.0,
#         # 'args': (16, 16)
#     },
#
# }
# app.conf.timezone = 'UTC'

