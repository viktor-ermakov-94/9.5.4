from django.contrib import admin

# импортируем наши модели
from .models import Appointment

# и зарегистрируем их
admin.site.register(Appointment)

