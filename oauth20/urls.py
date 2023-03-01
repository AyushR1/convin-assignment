from django.urls import path

from . import views

urlpatterns = [
    path('calendar/init/', views.GoogleCalendarInitView, name='google_permission'),
    path('', views.index, name='index'),
]