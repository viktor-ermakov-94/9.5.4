# импортируем декоратор для получения сигналов
from datetime import date, timedelta

from allauth.utils import build_absolute_uri
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver

# импортируем модуль для отправки писем
from django.core.mail import send_mail, EmailMultiAlternatives

# импортируем сигнал реагирующий на создание новой модели (в данном случае - новости)
from django.db.models.signals import post_save, m2m_changed

# импортируем модель Post, так как сигнал будет подключаться к ней

from django.shortcuts import render
from django.http import request
from django.template.loader import render_to_string

from . import views
from .models import Post, Category

# загружаем модуль для проверки, если пользователь зарегистрировался
from allauth.account.signals import user_signed_up, email_confirmed


# отправка писем для подписчиков по категориям
from NewsPortal import settings


@receiver(m2m_changed, sender=Post.post_category.through)
def new_post(sender, action, instance, **kwargs):
    # если проходит команда post_add, то есть добавляется новость,
    # то выполняются следующие действия:
    if action == 'post_add':
        # достаём путь news/id новости
        post_url = instance.get_absolute_url()
        # достаём ip адрес домена, добавляем к нему порт и http:// и добавляем путь до самой новости
        full_url = ''.join(['http://', get_current_site(None).domain, ':8000']) + post_url

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
                    message=f'{instance.date_created.strftime("%d %m %Y")} - {instance.content[:50]}, {full_url}',
                    from_email='FPW-13@yandex.ru',
                    recipient_list=[cat.email]
                )


# отправка письма после подтверждения электронной почты
@receiver(email_confirmed)
def user_signed_up(request, email_address, **kwargs):
    # отправляется письмо пользователю, чья почта была подтверждена
    send_mail(
        subject=f'Dear {email_address.user} Welcome to my News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='FPW-13@yandex.ru',
        recipient_list=[email_address.user.email]
    )

#
# # еженедельная рассылка
# def week_post():
#     if date.today().weekday() == 2:  # если сегодня понедельник
#         start = date.today() - timedelta(7)  # вычтем от сегодняшнего дня 7 дней. Это будет началом диапазона выборки
#         # дат
#         finish = date.today()  # сегодняшний день - конец диапазона выборки дат
#
#         # список постов, отфильтрованный по дате создания в диапазоне start и finish
#         list_of_posts = Post.objects.filter(date_created__range=(start, finish))
#
#         # формируем список из id постов за неделю
#         list_of_posts_ids = []
#         for i in list_of_posts:
#             list_of_posts_ids.append(i.id)
#
#         subscribers = []  # пустой список, куда будут записаны подписчики
#         for i in list_of_posts:
#             print(i.post_category.values("subscribers"))  # печатает всех подписчиков на выбранные новости
#             subscribers.append(
#                 i.post_category.values("subscribers"))  # формируем список из всех подписчиков по всем постам
#
#         subscribers_id = []  # пустой список для сбора данных по подписчикам
#         for i in subscribers:  # пробегаемся по всем подписчикам всех постов
#             for j in i:  # пробегаемся по подписчикам каждого поста
#                 subscribers_id.append(j['subscribers'])  # вынимаем из этих словарей с подписчиками только их id
#         subscribers_id = list(
#             set(subscribers_id))  # убираем дубликаты id, чтобы сделать чистый список из номеров id подписчиков
#
#         for posts in list_of_posts:  # для каждого поста из списка постов печатаем категории, с которыми связан пост
#             posts_list = posts.post_category.all()
#
#         for subscribers in subscribers_id:
#             for id in list_of_posts_ids:
#                 for i in Post.objects.get(id=id).post_category.all():
#                     users = [i.subscribers.filter(id=subscribers)]
#                     for u in users:
#
#                         send_mail(
#                             subject=f'Check new posts.',
#                             message=f'{list_of_posts}',
#                             from_email='FPW-13@yandex.ru',
#                             recipient_list=[u.email]
#                         )
# еженедельная рассылка
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
        # print('Еженедльная рассылка успешна отправлена')
        # print(subscribers_emails)