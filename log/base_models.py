from django.contrib.auth import get_user_model
from django.db import models

from file.models import File


class BaseLogModel(models.Model):
    id = models.BigAutoField(
        primary_key=True
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
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    ip_address = models.GenericIPAddressField(
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
        abstract = True
        ordering = ('-timestamp',)


