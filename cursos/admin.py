from django.contrib import admin

from .models import Cursos, ProgressoCurso

class CursosAdmin(admin.ModelAdmin):

    list_display = ['title', 'slug' ,'created_at']
    search_fields = ['title', 'slug']

admin.site.register(Cursos, CursosAdmin)

class ProgressoCursoAdmin(admin.ModelAdmin):

    list_display = ['user', 'curso', 'progresso']
    search_fields = ['user', 'curso']

admin.site.register(ProgressoCurso, ProgressoCursoAdmin)
