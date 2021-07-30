# импортируем декоратор для получения сигналов
from allauth.utils import build_absolute_uri
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver

# импортируем модуль для отправки писем
from django.core.mail import send_mail

# импортируем сигнал реагирующий на создание новой модели (в данном случае - новости)
from django.db.models.signals import post_save, m2m_changed

# импортируем модель Post, так как сигнал будет подключаться к ней

from django.shortcuts import render
from django.http import request

from . import views
from .models import Post

# загружаем модуль для проверки, если пользователь зарегистрировался
from allauth.account.signals import user_signed_up, email_confirmed


# отправка писем для подписчиков по категориям
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
