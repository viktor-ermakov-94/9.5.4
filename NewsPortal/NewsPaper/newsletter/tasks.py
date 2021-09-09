from celery import shared_task
from NewsPaper.models import Post, Category
from datetime import date, timedelta
from django.contrib.auth.models import User

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPortal import settings

from NewsPaper.signals import week_post_2


# @shared_task
# def hello():
#
#     print("Hello, world!")
#
#
# @shared_task
# def send():
#     send_mail(
#         subject='Hello Mr. Petr',
#         message='This is a test email from your friend',
#         from_email='FPW-13@yandex.ru',
#         recipient_list=['FPW-13@yandex.ru','expowheella@gmail.com'],
#     )
#

# @shared_task
# def newsletter():
#     week_post_2

@shared_task
def week_post():
    # if date.today().weekday() == 3:  # если сегодня среда
    start = date.today() - timedelta(7)  # вычтем от сегодняшнего дня 7 дней. Это будет началом диапазона выборки
    # дат
    finish = date.today()  # сегодняшний день - конец диапазона выборки дат

    # список постов, отфильтрованный по дате создания в диапазоне start и finish
    list_of_posts = Post.objects.filter(date_created__range=(start, finish))
    print(list_of_posts)
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
        print('Еженедльная рассылка успешна отправлена')
        print(subscribers_emails)
