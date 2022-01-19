from typing import List
from cursos.models import Cursos, ProgressoCurso
from videos.models import WatchedVideo, Videos
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .forms import Contact

from django.contrib.auth.models import User

@login_required(login_url='accounts:login')
def index(request):
    qtd_videos_assistidos = WatchedVideo.objects.filter(user=request.user).count()
    total_videos = Videos.objects.all().count()

    cursos = Cursos.objects.all()
    cursos_concluidos = ProgressoCurso.objects.filter(user=request.user,progresso=100)
    cursos_andamento = ProgressoCurso.objects.filter(user=request.user,progresso__range=[1,99])

    for i in cursos.values('id'):

        verifica_curso_iniciado = ProgressoCurso.objects.filter(user=request.user, curso=i['id'])

        if verifica_curso_iniciado:
            qtd_video_por_curso = Videos.objects.filter(curso=i['id']).count()
            qtd_video_assistido_por_curso = WatchedVideo.objects.filter(user=request.user, curso=i['id']).count()
            try:
                progresso_por_curso = (qtd_video_assistido_por_curso / qtd_video_por_curso) * 100
            except:
                progresso_por_curso = 0
            verifica_curso_iniciado.update(progresso=progresso_por_curso)
        else:
            grava_progresso = ProgressoCurso(user=request.user, curso=i['id'], progresso=0)
            grava_progresso.save()

    cursos_nao_iniciados = ProgressoCurso.objects.filter(user=request.user,progresso=0)

    context = {
        'progresso': '{:.2f}'.format((qtd_videos_assistidos/total_videos) * 100),
        'cursos': cursos,
        'cursos_andamento': cursos_andamento,
        'cursos_concluidos': cursos_concluidos,
        'cursos_nao_iniciados': cursos_nao_iniciados
    }
    
    return render(request, 'index.html', context)

@login_required(login_url='accounts:login')
def contact(request):
    context = {}
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail()
            form = Contact()
    else:
        form = Contact()

    context['form'] = form

    template_name = 'contato.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def config(request):
	return render(request, 'config.html')

@login_required(login_url='accounts:login')
def sessiongamer(request):

    videos_assistidos = WatchedVideo.objects.filter(user=request.user).values('title')
    qtd_videos_assistidos = WatchedVideo.objects.filter(user=request.user).count()
    total_videos = Videos.objects.all().count()

    lista_videos = []
    for i in range(qtd_videos_assistidos):
        lista_videos.append(videos_assistidos[i]['title'])
   
    context = {
        'videos': lista_videos,
        'progresso': '{:.2f}'.format((qtd_videos_assistidos/total_videos) * 100)
    }

    return render(request, 'session_gamer.html', context)

@login_required(login_url='accounts:login')
def alterar_tema(request):
	return render(request, 'alterar_tema.html')

@login_required(login_url='accounts:login')
def buscar(request):

    lista_videos = Videos.objects.filter(title__icontains=request.GET['buscar'])
    lista_cursos = Cursos.objects.filter(title__icontains=request.GET['buscar'])
    lista_videos_assistidos = WatchedVideo.objects.filter(user=request.user, title__icontains=request.GET['buscar'])

    lista_progresso_curso = ProgressoCurso.objects.filter(user=request.user)

    context = {
        'videos': lista_videos,
        'cursos': lista_cursos,
        'busca': request.GET['buscar'],
        'videos_assistidos': lista_videos_assistidos,
        'lista_progresso_curso': lista_progresso_curso,
    }

    return render(request, 'buscar.html', context)

@login_required(login_url='accounts:login')
def details(request, slug):
    video = get_object_or_404(Videos,slug=slug)

    context = {
        'video': video,
    }
    template_name = 'details_buscar_videos.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def video_assistido(request, title): 
    video = get_object_or_404(Videos,title=title)
    context = {
        'video': video,
    }

    curso = Videos.objects.filter(title=title).values('curso')
    id_curso = curso[0]['curso']

    
    verifica_video_assistido = WatchedVideo.objects.filter(user=request.user, title=video) #realiza consulta no bd para ver se o user current já assistiu o video em questão
    if verifica_video_assistido:
        pass
    else:    
        video_assistido = WatchedVideo(user=request.user, title=video, curso=curso)
        video_assistido.save()

        
        qtd_video_por_curso = Videos.objects.filter(curso=id_curso).count()
        qtd_video_assistido_por_curso = WatchedVideo.objects.filter(user=request.user, curso=id_curso).count()
        progresso_por_curso = (qtd_video_assistido_por_curso / qtd_video_por_curso) * 100

        verifica_curso_iniciado = ProgressoCurso.objects.filter(user=request.user, curso=id_curso)

        if verifica_curso_iniciado:
             verifica_curso_iniciado.update(progresso=progresso_por_curso)
        else:
            grava_progresso = ProgressoCurso(user=request.user, curso=id_curso, progresso=progresso_por_curso)
            grava_progresso.save()
        

    return render(request, 'video_assistido.html', context)

@login_required(login_url='accounts:login')
def ranking(request):

    dict_ranking = {}
    for u in User.objects.all().values('username'):
        dict_ranking[u['username']] = WatchedVideo.objects.filter(user=u['username']).count()

    dict_ranking = sorted(dict_ranking.items(), key=lambda x: x[1], reverse=True)

    context = {
        'ranking': dict_ranking
    }

    return render(request, 'ranking.html', context)