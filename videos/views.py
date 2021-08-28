from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from .models import Videos, WatchedVideo
from cursos.models import Cursos

@login_required(login_url='accounts:login')
def videos(request):
    videos = Videos.objects.all()
    template_name = 'videos.html'
    context = {
        'videos': videos
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def details(request, slug):
    video = get_object_or_404(Videos,slug=slug)
    videos = Videos.objects.all()
    context = {
        'video': video,
        'videos': videos
    }
    template_name = 'details_videos.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def video_assistido(request, title): 
    video = get_object_or_404(Videos,title=title)
    videos = Videos.objects.all()

    context = {
        'video': video,
        'videos': videos
    }

    verifica_video_assistido = WatchedVideo.objects.filter(user=request.user, title=video) #realiza consulta no bd para ver se o user current já assistiu o video em questão
    if verifica_video_assistido:
        pass
    else:    
        video_assistido = WatchedVideo(user=request.user, title=video)
        video_assistido.save()

    return render(request, 'video_assistido.html', context)