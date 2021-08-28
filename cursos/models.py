from django.db import models

class CursosManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Cursos(models.Model):
    
    title = models.CharField('Título Curso', max_length=255)

    slug = models.SlugField('Atalho', null=False, unique=True)

    description = models.TextField('Descrição Simples', blank=True)

    created_at = models.DateTimeField('Criado em:', auto_now_add=True)

    objects = CursosManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Cursos'
        verbose_name_plural = 'Cursos'
        ordering = ['created_at']
