from django.contrib import admin

from .models import DownloadLog, ChangeLog
# Register your models here.

admin.site.register(DownloadLog)
admin.site.register(ChangeLog)