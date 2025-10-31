from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from file.serializers import FileUploadSerializer


class TestFileUploadSerializer(TestCase):

    def test_validate_file_valid(self):
        valid_file = SimpleUploadedFile('test.txt', b'test')
        serializer = FileUploadSerializer(data={'file': valid_file})
        validate_file = serializer.validate_file(valid_file)
        self.assertEqual(validate_file, valid_file)

    def test_validate_file_large_size_invalid(self):
        max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        large_file = SimpleUploadedFile('test.txt', b'test' * (max_size + 1))
        serializer = FileUploadSerializer(data={'file': large_file})
        with self.assertRaises(ValidationError):
            serializer.validate_file(large_file)

    def test_validate_file_allowed_extensions_invalid(self):
        invalid_extension_file = SimpleUploadedFile('test.exe', b'test')
        serializer = FileUploadSerializer(data={'file': invalid_extension_file})
        with self.assertRaises(ValidationError):
            serializer.validate_file(invalid_extension_file)

    def test_validate_expires_at_valid(self):
        serializer = FileUploadSerializer()

        future_time = timezone.now() + timezone.timedelta(days=1)
        result = serializer.validate_expires_at(future_time)
        self.assertEqual(result, future_time)

    def test_validate_expires_at_invalid(self):
        serializer = FileUploadSerializer()

        past_time = timezone.now() - timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            serializer.validate_expires_at(past_time)
