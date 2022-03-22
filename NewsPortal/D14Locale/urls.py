from django.urls import path, include
# импортируем наше представление
from .views import HomePageView, set_timezone

urlpatterns = [
    path('', HomePageView.as_view()),
    path('tz/', set_timezone, name='set_timezone'),
]