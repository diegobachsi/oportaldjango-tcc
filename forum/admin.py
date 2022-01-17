from django.contrib import admin

from .models import Forum, AnswerForum

class ForumAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'curso', 'title', 'slug' ,'created_at']
    search_fields = ['title', 'slug']

admin.site.register(Forum, ForumAdmin)

class AnswerForumAdmin(admin.ModelAdmin):

    list_display = ['user', 'id_topico_forum', 'answer']
    search_fields = ['user', 'id_topico_forum', 'answer']

admin.site.register(AnswerForum, AnswerForumAdmin)
