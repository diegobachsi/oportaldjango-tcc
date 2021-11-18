from django.contrib import admin

from .models import Videos, WatchedVideo

class VideosAdmin(admin.ModelAdmin):

    list_display = ['title', 'slug', 'curso', 'watched_at']
    search_fields = ['title', 'slug']

admin.site.register(Videos, VideosAdmin)

class WatchedVideoAdmin(admin.ModelAdmin):

    list_display = ['user', 'title', 'curso']
    search_fields = ['user', 'title']

admin.site.register(WatchedVideo, WatchedVideoAdmin)