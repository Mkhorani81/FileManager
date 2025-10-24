from django.contrib import admin

from .models import File, Link


# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'max_downloads', 'download_count', 'status', 'uploaded_at', 'expires_at')
    list_filter = ('owner', 'status', 'expires_at')
    ordering = ('-expires_at', 'max_downloads')

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('file', 'short_code', 'created_at')
    list_filter = ('file', 'created_at')
    ordering = ('-created_at',)