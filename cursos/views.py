from videos.models import Videos
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from .models import Cursos

@login_required(login_url='accounts:login')
def cursos(request):
    cursos = Cursos.objects.all()
    template_name = 'cursos.html'
    context = {
        'cursos': cursos
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def details(request, slug):

    curso = get_object_or_404(Cursos,slug=slug)
    cursos = Cursos.objects.all()
    context = {
        'curso': curso,
        'cursos': cursos,
    }
    template_name = 'details_cursos.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def videos_por_cursos(request, id):
    curso = Cursos.objects.filter(id=id)
    print(curso)
    videos = Videos.objects.filter(curso=id)
    template_name = 'videos_por_cursos.html'
    context = {
        'videos': videos,
        'cursos': curso
    }
    return render(request, template_name, context)