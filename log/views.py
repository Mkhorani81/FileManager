from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from log.models import DownloadLog
from log.serializers import DownloadLogSerializer


# Create your views here.

class DownloadLogViewSet(viewsets.ViewSet):
    """
    This is the view by which admin could get query from download logs.
    """

    permission_classes = [IsAdminUser]

    def list(self, request):
        queryset = DownloadLog.objects.all()
        serializer = DownloadLogSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def group_by(self, request):

        group_by = request.query_params.get('group_by')
        if group_by not in ['user', 'file']:
            return Response(
                {'detail': 'Invalid group_by value. Use "user", "file".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        download_logs = DownloadLog.objects.select_related('user', 'file').all()
        serializer = DownloadLogSerializer(download_logs, many=True)

        grouped = {}
        for item in serializer.data:
            key = str(item[group_by]) if item[group_by] else "Unknown"
            grouped.setdefault(key, []).append(item)

        return Response(grouped, status=status.HTTP_200_OK)
