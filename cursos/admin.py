from django.contrib import admin

from .models import Cursos

class CursosAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'slug' ,'created_at']
    search_fields = ['title', 'slug']

admin.site.register(Cursos, CursosAdmin)
