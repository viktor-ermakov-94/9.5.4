from datetime import datetime
from django.db import models


# Сначала мы создали модель записи на приём. Скелет, который будем использовать далее в вьюшках
# модель записи на приём
class Appointment(models.Model):
    # дата записи клиента
    date = models.DateField(default=datetime.utcnow, )
    # имя клиента
    client_name = models.CharField(max_length=200)
    # сообщение от клиента
    message = models.TextField()

    # функция, возвращающая имя клиента и его сообщение
    def __str__(self):
        return f'{self.client_name}: {self.message}'
