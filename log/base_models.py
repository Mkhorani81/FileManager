from django.contrib.auth import get_user_model
from django.db import models

from file.models import File


class BaseDownloadLog(models.Model):
    """
        Design this model to store information about a download of file by user
    """

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
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ('-timestamp',)
        index_together = [
            models.Index('user', 'file')
        ]
        verbose_name = 'Download Log'
        verbose_name_plural = 'Download Logs'
