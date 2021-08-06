### Отправка письма после подтверждения электронной почты
#### в файле signals.py
    @receiver(email_confirmed)
    def user_signed_up(request, email_address, **kwargs):
        # отправляется письмо пользователю, чья почта была подтверждена
        send_mail(
            subject=f'Dear {email_address.user} Welcome to my News Portal!',
            message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
            from_email='FPW-13@yandex.ru',
            recipient_list=[email_address.user.email]
        )


## D6.4 Subscribe
## Отправка писем при появлении новости соответствующей категории 

#### 1) я использовал шаблон post_details.html, куда добавил кнопку рядом с новостью ("Оформить подписку на подобные новости") 

    <td>
        <a class="nav-link" href="subscribe/">Оформить подписку на подобные новости </a>
    </td>

#### 2) после нажатия на эту кнопку, меня переносит по ссылке subscribe/
#### 3) далее срабатывает функция subscribe, которая прописана в urls/py

    ...
    path('<int:pk>/subscribe/', subscribe, name='subscription'),
    ...

#### 4) в файле NewsPaper\views.py добавляем функцию, которая запускается при нажатии на ссылку в шаблоне post_details.html
    
    # отправка писем для подписчиков по категориям
    @login_required
    def subscribe(request, **kwargs):  
        # request = <WSGIRequest: GET '/subscribe/'> - то есть к нам возвращается urls адрес,
        # который мы записали в html шаблоне кнопки

        pk = kwargs['pk']  # 0 то же самое можно записать, как: pk = kwargs.get('pk')
    
        my_post = Post.objects.get(id=pk).post_category.values()

        for i in my_post:
            post_cat_id = i['id']
 
        # находим объекты категории, с которыми связан данный пост,
        # и добавляем текущего пользователя в поле subscribers моделей
        Category.objects.get(id=post_cat_id).subscribers.add(request.user)
    
        subscribers = Category.objects.filter(subscribers=request.user)
        print(f"subscribed categories={subscribers}")
    
        for i in subscribers:
            print('Эта новость относится к категории:', i)
    
        print(my_post.filter(subscribers=request.user.id).exists())
    
        return redirect('/news')




#### 2. Создаем файл appointment\signals.py
в этом файле добавляем следующее:

#### 1) импортируем декоратор для получения сигналов
    from django.dispatch import receiver
#### 2) импортируем модуль для отправки писем менеджерам
    from django.core.mail import send_mail
#### 3) импортируем сигнал реагирующий на изменение поля ManyToMany в экземпляре модели
    from django.db.models.signals import m2m_changed
#### 4) импортируем модель Post, так как сигнал подключается к данной модели
    from .models import Post

#### 5) подключаемся к сигналу
    @receiver(m2m_changed, sender=Post.post_category.through)
    def new_post(sender, action, instance, **kwargs):
        # если проходит команда post_add, то есть добавляется новость,
        # то выполняются следующие действия:
        if action == 'post_add':
    
            # для каждого из экземпляров категорий созданной новости
            # (например,если у новости две категории, то для каждой из них)
            for each in instance.post_category.all():  # например в данном случае each -> sport, culture
                # потому что модель Category возвращает поле article_category, где как-раз хранятся значения sport и
                # culture instance - это экземпляр модели Category, и когда мы перебираем эти самые экземпляры,
                # то получаем доступ и к остальным полям. Поэтому в данном случае each представляет каждый
                # экземпляр instance
    
                # теперь мы снова перебираем поля экземпляра instance, который представлен переменной each
                # each.subscribers даёт нам доступ к полю subscribers, и следом вызывая cat.email, мы уже проваливаемся в
                # модель пользователя User к его родительскому классу, к полю email    
                for cat in each.subscribers.all():
                    # 1) cat = sport
                    # 2) cat = culture
    
                    send_mail(
                        subject=f'A new post named "{instance.title}" is created!',
                        message=f'{instance.date_created.strftime("%d %m %Y")} - {instance.content[:10]}',
                        from_email='FPW-13@yandex.ru',
                        recipient_list=[cat.email]
                    )
    
                    print(cat.email)


    <------------------------Примечания-------------------------->

    @receiver - это декоратор, который подключает приемник к сигналу.
    
    сигнал от создания -> post_save экземпляра Appointment
    
    класс Appointment является отправителем сигнала
    
    sender - модель, к которой подключен сигнал
    
    instance - экземпляр класса (модели) в базе данных (сущность)
    
    created - True, если модель была только что создана, False - если уже существует в базе данных
    
    **kwargs - сопутствующие словари, которые необходимо распаковать
    <------------------------Примечания-------------------------->

#### 6) в файл NewsPaper\apps.py добавляем функцию ready:

    def ready(self):
        import NewsPaper.signals
        
        
        
        
        
 ## D6.5 Еженедельная рассылка
 
#### 1. Один раз в неделю по понедельникам отправляются письма подписчикам с появившимися новостями по категориям подписки.
Для этого создадим файл:
#### NewsPaper/management/commands/runapscheduler.py
    import logging
     
    from django.conf import settings
    
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger
    from django.core.management.base import BaseCommand
    from django_apscheduler.jobstores import DjangoJobStore
    from django_apscheduler.models import DjangoJobExecution
    from django_apscheduler import util
    
    # загружаем функцию которую мы написали в signals.py
    from NewsPaper.signals import week_post_2
    # from NewsPortal.NewsPaper.models import Post
    
    logger = logging.getLogger(__name__)
    
    
    def my_job():
        # Your job processing logic here...
        print('Hello from jobscheduler!')
        
        # здесь вызываем написанную нами функцию в NewsPaper/signals.py
        week_post_2()
        pass
    
    
    # The `close_old_connections` decorator ensures that database connections, that have become
    # unusable or are obsolete, are closed before and after our job has run.
    @util.close_old_connections
    def delete_old_job_executions(max_age=604_800):
        """
        This job deletes APScheduler job execution entries older than `max_age` from the database.
        It helps to prevent the database from filling up with old historical records that are no
        longer useful.
    
        :param max_age: The maximum length of time to retain historical job execution records.
                        Defaults to 7 days.
        """
        DjangoJobExecution.objects.delete_old_job_executions(max_age)
    
    
    class Command(BaseCommand):
        help = "Runs APScheduler."
    
        def handle(self, *args, **options):
            scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
            scheduler.add_jobstore(DjangoJobStore(), "default")
    
            scheduler.add_job(
                my_job,
                trigger=CronTrigger(week="*/1"),  # Every 1 week
                id="my_job",  # The `id` assigned to each job MUST be unique
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job 'my_job'.")
    
            scheduler.add_job(
                delete_old_job_executions,
                trigger=CronTrigger(
                    day_of_week="mon", hour="00", minute="00"
                ),  # Midnight on Monday, before start of the next work week.
                id="delete_old_job_executions",
                max_instances=1,
                replace_existing=True,
            )
            logger.info(
                "Added weekly job: 'delete_old_job_executions'."
            )
    
            try:
                logger.info("Starting scheduler...")
                scheduler.start()
            except KeyboardInterrupt:
                logger.info("Stopping scheduler...")
                scheduler.shutdown()
                logger.info("Scheduler shut down successfully!")

#### в settings.py добавим следующие параметры:

    INSTALLED_APPS = [
    ...
    # добавляем приложение для запуска периодических задач
    'django_apscheduler',
    ]

    ...

    # Указываем формат даты для scheduler
    APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
    
    # Время на выполнение задачи (задача снимается, если не успеет выполниться)
    APSCHEDULER_RUN_NOW_TIMEOUT = 25  # seconds

 #### 2. Напишем функцию, которая отвечает за формирование и отправку писем:
    def week_post_2():
        if date.today().weekday() == 1:  # если сегодня понедельник
            start = date.today() - timedelta(7)  # вычтем от сегодняшнего дня 7 дней. Это будет началом диапазона выборки
            # дат
            finish = date.today()  # сегодняшний день - конец диапазона выборки дат
    
            # список постов, отфильтрованный по дате создания в диапазоне start и finish
            list_of_posts = Post.objects.filter(date_created__range=(start, finish))
    
            # все возможные категории
            categories = Category.objects.all()
    
            # возьмём все возможные категории и пробежимся по ним
            for category in categories:
                # создадим список, куда будем собирать почтовые адреса подписчиков
                subscribers_emails = []
                # из списка всех пользователей
                for user in User.objects.all():
                    # отфильтруем только тех, кто подписан на конкретную категорию, по которой идёт выборка
                    # делаем это за счёт того, что в модели Category в поле subscribers
                    # мы добавили имя обратной связи от User к Category, чтобы получить доступ
                    # ко всем связанным объектам пользователя --> related_name='subscriber'
                    user.subscriber.filter(article_category=category)
                    # добавляем в список адреса пользователей, подписанных на текущую категорию
                    subscribers_emails.append(user.email)
    
                    # укажем контекст в виде словаря, который будет рендерится в шаблоне week_posts.html
                    html_content = render_to_string('NewsPaper/week_posts.html',
                                                    {'posts': list_of_posts, 'category': category})
                    
                    # формируем тело письма
                    msg = EmailMultiAlternatives(
                        subject=f'Все новости за прошедшую неделю',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=subscribers_emails,
                    )
                    msg.attach_alternative(html_content, "text/html")  
                    msg.send()  # отсылаем

#### 3. в папке templates/NewsPaper создадим шаблон week_posts.html, который будет отвечать за формирование содержания html-письма:

    <!DOCTYPE html>
    {% load i18n %}
    
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h1 style="color:#0000ff">{% trans "Дайджест новостей за прошедшую неделю в категории" %} {{ category }}!</h1>
    <table>
        {% for post in posts %}
        <tr>
            <td>
                <a href="http://localhost:8000/news/{{ post.id }}">{{ post.title }}</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    </body>
    </html>
