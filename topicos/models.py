from django.db import models

class TopicsManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Topics(models.Model):
    
    name = models.CharField('Nome', max_length=255)

    slug = models.SlugField('Atalho', null=False, unique=True)

    description = models.TextField('Descrição Simples', blank=True)

    about = models.TextField('Sobre a Atividade', blank=True)

    start_date = models.DateField('Data de Início', null=True, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = TopicsManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Topicos'
        verbose_name_plural = 'Topicos'
        ordering = ['created_at']
