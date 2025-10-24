from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils import generate_short_code


class FileQuerySet(models.QuerySet):
    """
    This is a Queryset in which customizes the queryset method
    """

    def active(self):
        from .models import File
        now = timezone.now()
        return self.filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=now),
        ).exclude(status=File.Status.DELETED)

    def all_objects(self):
        return self.all()


class FileManager(models.Manager):
    def get_queryset(self):
        return FileQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def all_objects(self):
        return self.get_queryset().all_objects()


class LinkQuerySet(models.QuerySet):
    """To customize the queryset method for link model and adding requirement methods in"""

    def generate_download_link(self, file, length=16):
        """Create unique short code for download"""
        for _ in range(10):
            code = generate_short_code(length)
            if not self.filter(short_code=code).exists():
                return self.create(file=file, short_code=code)
        raise RuntimeError('Unable to generate unique short code')


class LinkManager(models.Manager):
    def get_queryset(self):
        return LinkQuerySet(self.model, using=self._db)

    def generate_download_link(self, file, length=16):
        return self.get_queryset().generate_download_link(file, length)
