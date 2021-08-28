from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Topics

@login_required(login_url='accounts:login')
def topicos(request):
    topicos = Topics.objects.all()
    template_name = 'topicos.html'
    context = {
        'topicos': topicos
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def details(request, slug):
    topico = get_object_or_404(Topics,slug=slug)
    topicos = Topics.objects.all()
    context = {
        'topico': topico,
        'topicos': topicos
    }
    template_name = 'details.html'
    return render(request, template_name, context)



