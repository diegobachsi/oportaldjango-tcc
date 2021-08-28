from django.urls import path

from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.cursos, name='index'),
    path('<int:id>', views.videos_por_cursos, name='video_por_cursos'),
    path('<slug:slug>', views.details, name='details'),
]