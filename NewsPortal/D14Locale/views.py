import pytz
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

# импортируем функцию для перевода
from django.utils.translation import gettext as _

# импортируем часовые пояса
from django.utils import timezone
# импортируем стандартный модуль для работы с часовыми поясами
import pytz

class HomePageView(View):

    def get(self, request):
        string = _('Hello World')

        context = {
            'string': string
        }

        return HttpResponse(render(request, 'd14Locale/home.html', context))

common_timezones = {
    'Europe/London': 'Europe/London',
    'America/New_York': 'America/New_York',
}

def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/d14/tz')
    else:
        return render(request, 'd14Locale/home.html', {'timezones': common_timezones})
