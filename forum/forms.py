from django import forms
from cursos.models import Cursos

class FormForum(forms.Form):

    CHOICES = (
        ('4', 'Introdução HTML'),
        ('14', 'Introdução CSS'),
        ('24', 'Introdução JavaScript'),
        ('34', 'Introdução Python'),
        ('44', 'Curso de Django'),
        ('54', 'Git/Github para iniciantes'),
    )

    curso = forms.CharField(label='curso',widget=forms.Select(choices=CHOICES))
    title = forms.CharField(label='title', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Título'}))
    content = forms.CharField(label='content', widget=forms.Textarea(attrs={'placeholder': 'Conteúdo'}))
    answer = forms.CharField(label='answer', widget=forms.Textarea(attrs={'placeholder': 'Digite sua resposta'}))


    