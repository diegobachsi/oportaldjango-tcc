from django.db import models

class ForumManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(title__icontains=query) | \
            models.Q(content__icontains=query)
        )

class Forum(models.Model):

    user = models.CharField('Usuário', max_length=255)

    curso = models.CharField('Curso', max_length=255)
    
    title = models.CharField('Título Curso', max_length=255)

    slug = models.SlugField('Atalho', null=False, unique=True)

    content = models.TextField('Conteúdo', blank=True)

    created_at = models.DateTimeField('Criado em:', auto_now_add=True)

    objects = ForumManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Forum'
        verbose_name_plural = 'Forum'
        ordering = ['created_at']

class AnswerForum(models.Model):

    user = models.CharField('Usuário', max_length=100)

    id_topico_forum = models.CharField('Tópico Fórum', max_length=255)

    answer = models.TextField('Resposta', blank=True)

    created_at = models.DateTimeField('Criado em:', auto_now_add=True)

    def __str__(self):
        return self.answer