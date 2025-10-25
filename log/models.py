from django.contrib.auth import get_user, get_user_model
from django.db import models

from file.models import File


# Create your models here.

class DownloadLog(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    file = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='download_logs',
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='download_logs',
    )
    username_persistent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    requested_at = models.DateTimeField(
        auto_now_add=True,
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )
    short_code = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    success = models.BooleanField(
        default=False,
    )
    status_code = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )
    errors = models.TextField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-requested_at',)
        verbose_name = 'Download Log'
        verbose_name_plural = 'Download Logs'

    def __str__(self):
        return f'{self.file.name} - {self.username_persistent}'



class ChangeLog(models.Model):
    file = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='change_logs',
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='change_logs',
    )

