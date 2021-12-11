import math
from videos.models import Videos, WatchedVideo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from website.views import video_assistido

from .models import Cursos, ProgressoCurso

@login_required(login_url='accounts:login')
def cursos(request):

    lista_progresso_curso = ProgressoCurso.objects.filter(user=request.user)

    cursos = Cursos.objects.all()
    template_name = 'cursos.html'
    context = {
        'cursos': cursos,
        'lista_progresso_curso': lista_progresso_curso
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

    videos_assistidos = WatchedVideo.objects.filter(user=request.user, curso=id).values('title')

    duration = 0

    curso = Cursos.objects.filter(id=id)
    videos = Videos.objects.filter(curso=id)
    segundos = Videos.objects.filter(curso=id).values('segundos')

    lista_videos_assistidos = []

    for i in range(videos_assistidos.count()):
        lista_videos_assistidos.append(videos_assistidos[i]['title'])

    for i in range(videos.count()):
        duration += segundos[i]['segundos']
    
    template_name = 'videos_por_cursos.html'
    context = {
        'videos': videos,
        'cursos': curso,
        'duration': duration,
        'qtd_videos': videos.count(),
        'videos_assistidos': lista_videos_assistidos
    }
    return render(request, template_name, context)