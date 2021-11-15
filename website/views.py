from videos.models import WatchedVideo, Videos
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .forms import Contact


@login_required(login_url='accounts:login')
def index(request):
    qtd_videos_assistidos = WatchedVideo.objects.filter(user=request.user).count()
    total_videos = Videos.objects.all().count()

    context = {
        'progresso': '{:.0f}'.format((qtd_videos_assistidos/total_videos) * 100)
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
        'progresso': '{:.0f}'.format((qtd_videos_assistidos/total_videos) * 100)
    }

    return render(request, 'session_gamer.html', context)

@login_required(login_url='accounts:login')
def alterar_tema(request):
	return render(request, 'alterar_tema.html')

@login_required(login_url='accounts:login')
def buscar(request):

    lista_videos = Videos.objects.filter(title__icontains=request.GET['buscar'])

    context = {
        'videos': lista_videos,
        'busca': request.GET['buscar'],
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

    verifica_video_assistido = WatchedVideo.objects.filter(user=request.user, title=video) #realiza consulta no bd para ver se o user current já assistiu o video em questão
    if verifica_video_assistido:
        pass
    else:    
        video_assistido = WatchedVideo(user=request.user, title=video)
        video_assistido.save()

    return render(request, 'video_assistido.html', context)