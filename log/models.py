from django.contrib.auth import get_user, get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

from file.models import File
from .base_models import BaseLogModel


# Create your models here.

class DownloadLog(BaseLogModel):
    """
    Use BaseDownloadLog model:
        - In Base Model put main fields that refers in document
    """

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DELETED = 'deleted', 'Deleted'

    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='download_logs',
    )

    short_code = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        indexes = [
            models.Index(fields=['user', 'file']),
        ]
        verbose_name = 'Download Log'
        verbose_name_plural = 'Download Logs'

    def __str__(self):
        return f'{self.file} - {self.username_persistent}'

    def change_status(self, new_status):
        allowed_transition = {
            self.Status.ACTIVE: {self.Status.DELETED},
            self.Status.DELETED: set(),
        }

        if new_status == self.status:
            return

        if new_status not in allowed_transition.get(self.status, set()):
            raise ValueError(f"Transition from {self.status} to {new_status} not allowed!")

        self.status = new_status
        self.save(update_fields=['status'])


class ChangeLog(BaseLogModel):
    """
    Design this model to store information about a change of file by user:
    Store:
        - what has been changed,
        - when has been changed,
        - who has been changed,
        - on which model...
    """

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

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['content_type']),
            models.Index(fields=['object_id']),
        ]
        verbose_name = 'Change Log'
        verbose_name_plural = 'Change Logs'

    def __str__(self):
        return f'{self.content_type.name} - id:{self.object_id} - field:{self.username_persistent}'
