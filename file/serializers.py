from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from file.models import File, Link
from common.utils import file_extension


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        write_only=True,
    )

    class Meta:
        model = File
        fields = (
            'file', 'max_downloads', 'expires_at'
        )

    def validate_file(self, value):
        max_size = getattr(settings, 'MAX_FILE_SIZE_MB', 100) * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('File too large')

        allowed_extensions = file_extension(getattr(settings, 'FILES_ALLOWED_EXTENSIONS', None))
        if allowed_extensions:
            extensions = value.name.rsplit('.', 1)[-1].lower()
            if extensions not in [e.lower() for e in allowed_extensions]:
                raise serializers.ValidationError(f'File format not supported : {allowed_extensions}')

        return value

    def validate_expires_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError('Expire time should be in future')
        return value

    def create(self, validated_data):
        owner = self.context['request'].user
        file = File.objects.create(
            owner=owner,
            **validated_data
        )
        return file


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('short_code', 'created_at')


class FileListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(
    )
    link = LinkSerializer()

    class Meta:
        model = File
        fields = (
            'id', 'owner', 'file', 'uploaded_at', 'max_downloads',
            'expires_at', 'download_count', 'status', 'link'
        )
        read_only_fields = fields


class FileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('max_downloads', 'expires_at')
