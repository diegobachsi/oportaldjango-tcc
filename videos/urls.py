from django.urls import path

from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.videos, name='index'),
    path('<slug:slug>', views.details, name='details'),
    path('<title>', views.video_assistido, name='video_assistido')
]