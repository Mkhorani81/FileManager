from rest_framework import viewsets
from rest_framework.response import Response

from file.models import File
from file.serializers.admin import FileListSerializer


class FileAdminViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = File.objects.select_related('owner').prefetch_related('link').all()
        serializer = FileListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = File.objects.select_related('owner').prefetch_related('link').filter(id=pk)
        serializer = FileListSerializer(queryset, many=True)
        return Response(serializer.data)


