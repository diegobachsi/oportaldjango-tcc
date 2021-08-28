from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.cadastrar, name='register'),
    path('', views.logar, name='login'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]