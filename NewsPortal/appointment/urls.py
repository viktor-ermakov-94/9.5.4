# импортируем библиотеку для работы с путями urls
from django.urls import path
# импортируем наше представление
from .views import AppointmentView

app_name = 'appointment'

urlpatterns = [


    path('', AppointmentView.as_view(), name='make_appointment'),


]

