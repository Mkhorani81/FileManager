from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from file.models import File, Link
from file.paginations import FileAdminPagination
from file.serializers import FileListSerializer, FileUpdateSerializer

from file.serializers import FileUploadSerializer


class FileAdminViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)
    pagination_class = FileAdminPagination

    def create(self, request):
        ser_data = FileUploadSerializer(data=request.data, context={'request': request})
        if ser_data.is_valid():
            file_obj = ser_data.save()
            link = Link.objects.generate_download_link(file_obj)
            response = {
                'link': link.short_code,
                'file_id': file_obj.id,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        file = get_object_or_404(File, pk=pk)

        ser_data = FileUpdateSerializer(file, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response({
                'message': 'File updated successfully',
                'data': ser_data.data
            }, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = File.objects.select_related('owner').prefetch_related('link').all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        ser_data = FileListSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)

    def retrieve(self, pk=None):
        queryset = File.objects.select_related('owner').prefetch_related('link').filter(id=pk)
        ser_data = FileListSerializer(queryset, many=True)
        return Response(ser_data.data)

    def destroy(self, pk=None):
        file = File.objects.filter(id=pk)

        try:
            file.delete()
        except Exception as e:
            return Response(
                {'detail': f'Failed to delete file : {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {'detail': f'Successfully deleted file and related records'},
            status=status.HTTP_204_NO_CONTENT
        )
