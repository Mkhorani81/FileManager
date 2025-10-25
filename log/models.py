from django.contrib.auth import get_user, get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

from file.models import File
from .base_models import BaseDownloadLog


# Create your models here.

class DownloadLog(BaseDownloadLog):
    """
    Use BaseDownloadLog model:
        - In Base Model put main fields that refers in document
    """
    username_persistent = models.CharField(
        max_length=255,
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

    def __str__(self):
        return f'{self.file.name} - {self.username_persistent}'


class ChangeLog(models.Model):
    """
    Design this model to store information about a change of file by user:
    Store:
        - what has been changed,
        - when has been changed,
        - who has been changed,
        - on which model...
    """
    id = models.BigAutoField(
        primary_key=True
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='change_logs',
    )
    username_persistent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='change_logs',
    )
    object_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    field_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    old_value = models.TextField(
        null=True,
        blank=True,
    )
    new_value = models.TextField(
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-timestamp',)
        index_together = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['content_type']),
            models.Index(fields=['object_id']),
        ]
        verbose_name = 'Change Log'
        verbose_name_plural = 'Change Logs'

    def __str__(self):
        return f'{self.content_type.name} - id:{self.object_id} - field:{self.username_persistent}'
