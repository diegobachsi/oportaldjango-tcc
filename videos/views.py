from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from .models import Videos, WatchedVideo
from cursos.models import Cursos, ProgressoCurso

@login_required(login_url='accounts:login')
def videos(request):
    videos = Videos.objects.all()
    template_name = 'videos.html'
    context = {
        'videos': videos,
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def details(request, id, slug):
    video = get_object_or_404(Videos,slug=slug)
    videos = Videos.objects.filter(curso=id)
    curso = Cursos.objects.filter(id=id)

    videos_assistidos = WatchedVideo.objects.filter(user=request.user, curso=id).values('title')

    lista_videos_assistidos = []

    for i in range(videos_assistidos.count()):
        lista_videos_assistidos.append(videos_assistidos[i]['title'])

    context = {
        'video': video,
        'videos': videos,
        'cursos': curso,
        'videos_assistidos': lista_videos_assistidos
    }
    template_name = 'details_videos.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def video_assistido(request, id, title): 
    video = get_object_or_404(Videos,title=title)
    videos = Videos.objects.filter(curso=id)
    cursos = Cursos.objects.filter(id=id)

    videos_assistidos = WatchedVideo.objects.filter(user=request.user, curso=id).values('title')

    lista_videos_assistidos = []

    for i in range(videos_assistidos.count()):
        lista_videos_assistidos.append(videos_assistidos[i]['title'])

    context = {
        'video': video,
        'videos': videos,
        'cursos': cursos,
        'videos_assistidos': lista_videos_assistidos
    }

    verifica_video_assistido = WatchedVideo.objects.filter(user=request.user, title=video) #realiza consulta no bd para ver se o user current já assistiu o video em questão
    if verifica_video_assistido:
        pass
    else:    
        video_assistido = WatchedVideo(user=request.user, title=video, curso=id)
        video_assistido.save()

        qtd_video_por_curso = Videos.objects.filter(curso=id).count()
        qtd_video_assistido_por_curso = WatchedVideo.objects.filter(user=request.user, curso=id).count()
        progresso_por_curso = (qtd_video_assistido_por_curso / qtd_video_por_curso) * 100

        verifica_curso_iniciado = ProgressoCurso.objects.filter(user=request.user, curso=id)

        if verifica_curso_iniciado:
             verifica_curso_iniciado.update(progresso=progresso_por_curso)
        else:
            grava_progresso = ProgressoCurso(user=request.user, curso=id, progresso=progresso_por_curso)
            grava_progresso.save()

    return render(request, 'video_assistido.html', context)