from django.db import models
from cursos.models import Cursos

class VideosManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Videos(models.Model):

    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE)
    
    title = models.CharField('Título Vídeo', max_length=255)

    slug = models.SlugField('Atalho', null=False, unique=True)

    description = models.TextField('Descrição Simples', blank=True)

    watched_at = models.DateTimeField('Assistido em:', auto_now_add=True)

    objects = VideosManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Videos'
        verbose_name_plural = 'Videos'
        ordering = ['watched_at']

class WatchedVideo(models.Model):

    user = models.CharField('Usuário', max_length=100)

    title = models.CharField('Título Vídeo', max_length=255)

    def __str__(self):
        return self.title