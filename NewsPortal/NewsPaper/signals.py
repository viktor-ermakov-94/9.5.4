# импортируем декоратор для получения сигналов
from django.dispatch import receiver

# импортируем модуль для отправки писем
from django.core.mail import send_mail

# импортируем сигнал реагирующий на создание новой модели (в данном случае - новости)
from django.db.models.signals import post_save

# импортируем модель Post, так как сигнал будет подключаться к ней
from .models import Post


@receiver(signal=post_save, sender=Post)
def new_post(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=f'A new post named "{instance.title}" is created!',
            message=f'{instance.date_created.strftime("%d %m %Y")} - {instance.content[:10]}',
            from_email='FPW-13@yandex.ru',
            recipient_list=['FPW-13@yandex.ru', ]
        )
    print(f'{instance.date_created.strftime("%d %m %Y")} - new post is created')