from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail, mail_admins
from datetime import datetime
from .models import Appointment


# модель для обработки наших запросов на запись к врачу и сохранения новых записей в БД
class AppointmentView(View):
    # функция запроса, где аргументы: self = AppointmentView, унаследованная от класса View из библиотеки django.view
    # request = HTTP-запрос от браузера пользователя (т.е. запрос пользователя)
    def get(self, request, *args, **kwargs):
        # функция возвращает HTTP-ответ браузеру
        # request = HTTP-запрос от браузера пользователя
        # 'make_appointment.html' - шаблон, который должен использоваться при возврате HTTP-ответа
        return render(request, 'make_appointment.html', {})

    # функция отправки
    def post(self, request, *args, **kwargs):
        # создаем экземпляр модели Appointment, которую мы создали в models.py
        # которая хранит информацию о записи пользователя на встречу
        appointment = Appointment(
            # из формы, которую заполняет пользователь, через request отправляем дату, имя клиента, сообщение
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        # сохраняем в БД экземпляр модели Appointment
        appointment.save()

        # отправляем письмо
        # для этого используем готовую функцию из библиотеки send_mail, которую мы импортировали сюда
        # с её готовыми переменными аргументами
        send_mail(
            # имя клиента и дата записи будут в теме (с англ.: subject) письма для удобства
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',

            # сообщение с кратким описанием проблемы
            message=appointment.message,

            # здесь указываете почту, с которой будете отправлять (об этом попозже)
            from_email='FPW-13@yandex.ru',

            # здесь список получателей. Например, секретарь, сам врач и т. д.
            recipient_list=['', ]
        )

        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        # в итоге функция перекидывает на странцу шаблона
        return redirect('appointment:make_appointment')
