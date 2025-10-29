from rest_framework import serializers

from file.models import File, Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('short_code', 'created_at')


class FileListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    link = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = (
        'id', 'owner', 'file', 'uploaded_at', 'max_downloads', 'expires_at', 'download_count', 'status', 'link')
        read_only_fields = (
            'id', 'owner', 'file', 'uploaded_at', 'max_downloads', 'expires_at', 'download_count', 'status', 'link')
