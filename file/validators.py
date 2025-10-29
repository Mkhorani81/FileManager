from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_size(value):
    if value.size > int(settings.MAX_FILE_SIZE_MB) * 1024 * 1024:
        raise ValidationError('File should be less than 100 MB')
