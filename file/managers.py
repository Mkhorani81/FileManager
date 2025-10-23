from django.db import models
from django.db.models import Q
from django.utils import timezone

from .models import File

class FileQuerySet(models.QuerySet):
    """
    This is a Queryset in which customizes the queryset method
    """
    def active(self):
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