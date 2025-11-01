import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

from common.utils import file_extension

from .managers import FileManager, LinkManager
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

    objects = FileManager()

    class Meta:
        ordering = ('-uploaded_at',)
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['status']),
        ]
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return f'{self.id} - {self.file.name}'

    def is_expired(self):
        """define an object is expired or not"""
        if self.expires_at and timezone.now() >= self.expires_at:
            return True
        if self.status == self.Status.EXPIRED:
            return True
        return False

    def increment_download_count(self):
        """Increment download count automatically, using atomic transaction"""
        with transaction.atomic():
            File.objects.filter(pk=self.pk).update(download_count=F('download_count') + 1)
            self.refresh_from_db(fields=['download_count'])

    def can_download(self):
        if self.status != self.Status.ACTIVE:
            return False
        if self.is_expired():
            return False
        if self.max_downloads and self.download_count >= self.max_downloads:
            return False
        return True

    def change_status(self, new_status):
        """
        Enforce allow transition and log them

        Allowed transition:
            -Active -> Expired
            -Active -> Deleted
            -Expired -> Deleted
            -Deleted -> (NOT ALLOWED)
        """

        allowed_transtion = {
            self.Status.ACTIVE: {self.Status.EXPIRED, self.Status.DELETED},
            self.Status.EXPIRED: {self.Status.DELETED},
            self.Status.DELETED: set()
        }

        if new_status == self.status:
            return

        if new_status not in allowed_transtion.get(self.status, set()):
            raise ValueError(f"Transition from {self.status} to {new_status} now allowed!!!")

        old_status = self.status
        self.status = new_status
        self.save(update_fields=['status'])

        if new_status == self.Status.DELETED:
            if hasattr(self, 'link'):
                self.link.change_status(self.link.Status.DELETED)

            for log in self.download_logs.all():
                log.change_status(log.Status.DELETED)

        # TODO: adding log after creating its own model


class Link(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DELETED = 'deleted', 'Deleted'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file = models.OneToOneField(
        File,
        on_delete=models.CASCADE,
        related_name='link'
    )
    short_code = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    objects = LinkManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Short Link'
        verbose_name_plural = 'Short Links'

    def __str__(self):
        return f'{self.short_code} - {self.file.id}'

    def change_status(self, new_status):
        allowed_transtion = {
            self.Status.ACTIVE: {self.Status.DELETED},
            self.Status.DELETED: set()
        }

        if new_status == self.status:
            return

        if new_status not in allowed_transtion.get(self.status, set()):
            raise ValueError(f"Transition from {self.status} to {new_status} now allowed!!!")

        self.status = new_status
        self.save(update_fields=['status'])
