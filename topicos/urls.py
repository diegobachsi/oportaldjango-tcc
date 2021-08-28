from django.urls import path

from . import views

app_name = 'topicos'

urlpatterns = [
    path('', views.topicos, name='index'),
    path('<slug:slug>', views.details, name='details'),
]