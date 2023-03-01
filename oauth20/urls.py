from django.urls import path

from . import views

urlpatterns = [
    path('calendar/init/', views.GoogleCalendarInitView, name='google_permission'),
    path('calendar/redirect/', views.GoogleCalendarRedirectView, name='google_redirect'),
    path('', views.index, name='index'),
]