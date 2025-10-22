import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from decouple import config

from utils import file_extension

from .validators import validate_file_size


ALLOWED_EXTENSIONS = file_extension(settings.FILES_ALLOWED_EXTENSIONS)

# Create your models here.

class File(models.Model):
    """
    This is a model that stores files and medias,
    prepared some functions to implements features easily:
        - increment download count
        - check expire time
        - access to downloads
        - change status

    also check allowed transition too(for changing status)
    """

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        EXPIRED = 'expired', 'Expired'
        DELETED = 'deleted', 'Deleted'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
            validate_file_size
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    max_downloads = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
        ]
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    download_count = models.PositiveIntegerField(
        default=0,
        editable=False
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
