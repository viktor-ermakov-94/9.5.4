# импортируем декоратор для получения сигналов
from django.dispatch import receiver
# импортируем модуль для отправки писем менеджерам
from django.core.mail import mail_managers
# импортируем сигнал реагирующий на создание новой модели и удаление
from django.db.models.signals import post_save, post_delete
# импортируем модель Appointment
from .models import Appointment


# @receiver - это декоратор, который подключает приемник к сигналу
# сигнал от создания -> post_save экземпляра Appointment (в данном случае класс Appointment является отправителем сигнала)

@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    # sender - модель, к которой подключен сигнал
    # instance - экземпляр класса (модели) в базе данных (сущность)
    # created - True, если модель была только что создана, False - если уже существует в базе данных
    # **kwargs - сопутствующие словари, которые необходимо распаковать
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment is changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )
    print(f'{instance.client_name} {instance.date.strftime("%d %m %Y")}')


@receiver(post_delete, sender=Appointment)
def notify_managers_decline(sender, instance, *args, **kwargs):
    subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")} is deleted'
    mail_managers(
        subject=subject,
        message=f'the appointment with {instance.client_name} on {instance.date.strftime("%d %m %Y")} is deleted',
    )
    print(subject)
