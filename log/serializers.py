from rest_framework import serializers

from .models import DownloadLog


class DownloadLogSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='file.file.name', read_only=True)

    class Meta:
        model = DownloadLog
        fields = (
            'id', 'user', 'username_persistent', 'file', 'file_name',
            'short_code', 'timestamp', 'ip_address', 'success', 'status', 'status_code', 'errors'
        )
        read_only_fields = fields
