from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from file.models import File, Link
from file.paginations import FileAdminPagination
from file.serializers import FileListSerializer, FileUpdateSerializer

from file.serializers import FileUploadSerializer


class FileAdminViewSet(viewsets.ViewSet):
    """
    This is the viewset for file that only admin access to.

    The methods in view:
        - create new file (upload file directly)
            -fields (file, max_downloads, expires_at)
        - partial_update (edit Meta-data)
            -fields (max_downloads, expires_at)
        -list (get all files)

        - retrieve (get one file)
            - fields (primary key of specific file)
        -destroy (delete file) -> using soft deleted.
            - fields (primary key of specific file)
    """
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

    def retrieve(self, request, pk=None):
        queryset = File.objects.select_related('owner').prefetch_related('link').filter(id=pk)
        ser_data = FileListSerializer(queryset, many=True)
        return Response(ser_data.data)

    def destroy(self, request, pk=None):

        try:
            file = File.objects.get(id=pk)
            file.change_status(File.Status.DELETED)
            return Response(
                {'detail': 'Successfully deleted file and related records'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'detail': f'Failed to delete file : {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


