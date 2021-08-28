from videos.models import WatchedVideo, Videos
from django.shortcuts import render
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