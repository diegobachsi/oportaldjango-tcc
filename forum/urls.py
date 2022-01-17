from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_index, name='index'),
    path('<slug:slug>', views.forum, name='details'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('edit_final/<int:id>', views.edit_final, name='edit_final'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('answer/<int:id>', views.answer, name='answer'),
    path('delete_answer/<int:id>', views.delete_answer, name='delete_answer'),
    path('edit_answer/<int:id>', views.edit_answer, name='edit_answer'),
    path('edit_final_answer/<int:id>', views.edit_final_answer, name='edit_final_answer'),
    #path('<int:id>', views.forum_por_cursos, name='forum_por_cursos'),
]