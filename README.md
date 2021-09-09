

### D7.5. Создание задач по расписанию Celery+Redis+Docker+Django

1. Войти в виртуальное окружение:


    $ source virtualenv/bin/activate

2. Установить _Celery_:


    (virtualenv) $ pip3 install celery

3. В директории проекта добавить файл _celery.py_ рядом с _settings.py_.
   
4. В _celery.py_ добавить следующее:
   
    
    import os
    from celery import Celery
     
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
     
    app = Celery('project_name')
    app.config_from_object('django.conf:settings', namespace = 'CELERY')
    
    app.autodiscover_tasks()

    app.conf.beat_schedule = {
    
        'action_every_monday_8am': {
            'task': 'NewsPaper.newsletter.tasks.week_post',
            'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    
        },
    }

<i> В первую очередь мы импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery.

Второй строчкой мы связываем настройки Django с настройками Celery через переменную окружения.

Далее мы создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации. 

Мы также указываем пространство имен, чтобы Celery сам находил все необходимые настройки в общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***».

Последней строчкой мы указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
</i>

5. Добавить следующие строки в файл `__init__.py` (рядом с _settings.py_):


    from .celery import app as celery_app
    
    __all__ = ('celery_app',)

6. Настроить _Celery_ по инструкции “First Steps With Django”:
В файле _settings.py_ добавить:


    CELERY_TIMEZONE = "Europe/Moscow"
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60

7. Далее нам нужно настроить поддержку _Redis_ в _Python_ и _Celery_. Вновь зайдите в виртуальное окружение и установите следующие пакеты:


    (virtualenv) $ pip3 install redis
    (virtualenv) $ pip3 install -U "celery[redis]"
 
8. Далее мы должны добавить некоторые настройки в конфигурацию проекта (_settings.py_), дописав следующие строки:


    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

9. Подключить tasks, чтоб <i>Celery</i> их нашёл (опционально):


    CELERY_IMPORTS = (
         'NewsPaper.newsletter.tasks',
    )

10. В папке проекта создать файл <i>docker-compose.yml</i> и добавим туда следующие строки:
    

    version: "3"
    
    
    services:
     redis:
       image: redis
       ports:
         - "6379:6379"
    
11. Установить _django-celery-beat_, _django-celery-results_

12. Добавить в _settings.py_
    

    INSTALLED_APPS = [
       ...
    
    'django_celery_beat',
    'django_celery_results',
    
    
    ]

		
### Для запуска задач по расписанию необходимо сделать следующее:

**Терминал 1: $ python manage.py runserver**

**Терминал 2: $ docker-compose up**

**Терминал 3: $ celery -A NewsPortal beat**

**Терминал 4: $ celery -A NewsPortal worker -l INFO --pool=solo**

##Дополнительные материалы:
Периодические задачи: [https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)

First Steps With Django: [https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html?highlight=Django](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html?highlight=Django)

Настройка Docker, Celery для очереди задач: [https://www.youtube.com/watch?v=hQEHONHcF2c&list=LL&index=2](https://www.youtube.com/watch?v=hQEHONHcF2c&list=LL&index=2)

Команды для запуска Celery: [https://medium.com/analytics-vidhya/python-celery-explained-for-beginners-to-professionals-part-3-workers-pool-and-concurrency-ef0522e89ac5](https://medium.com/analytics-vidhya/python-celery-explained-for-beginners-to-professionals-part-3-workers-pool-and-concurrency-ef0522e89ac5)
