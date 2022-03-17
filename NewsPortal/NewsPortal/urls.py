from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    ]

# запаковывем все пути в i18n_patterns для локализации
urlpatterns += i18n_patterns(
    path('d14/', include('D14Locale.urls')),

    # чтобы адреса в будущем написанных нами страничек были доступны
    # нам для перехода по ним, добавим путь:
    path('pages/', include('django.contrib.flatpages.urls')),

    # чтобы все адреса из файла NewsPaper/urls.py
    # сами автоматически подключались когда мы их добавим.
    path('news/', include('NewsPaper.urls')),
    path('', include('NewsPaper.urls')),

    path('accounts/', include('allauth.urls')),

    path('make_appointment/', include('appointment.urls', namespace='appointment')),

    # чтобы по дефолту закидывало сразу на русскую страницу, добавляем строку:
    path('i18n/', include('django.conf.urls.i18n')),

    # отключаем отображение языка по умолчанию
    prefix_default_language=True,
)

    #path('appointment/', include(('appointment.urls', 'appointment'), namespace='appointment')),


# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns