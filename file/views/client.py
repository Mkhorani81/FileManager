from django.db import transaction
from django.http import FileResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from file.models import Link
from file.serializers import FileUploadSerializer

from log.mixins import DownloadLoggingMixin


class FileUploadView(APIView):
    """
    This view used to upload new file,
    The parameters:
        - file (File field with specific format could be customized in config file)
        - max_downloads -> (Integer field)
        - expires_at -> (Datetime field)

        other parameters fill out automatically

    HTTP methods which allowed:
        - POST
    """

    serializer_class = FileUploadSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            file_obj = serializer.save()
            link = Link.objects.generate_download_link(file_obj)
            file_url = reverse('file:file-download', args=[link.short_code])
            response = {
                'link': file_url,
                'file_id': file_obj.id,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FileDownloadView(DownloadLoggingMixin, APIView):
    """
    This view used to download a file,

    The parameters:
        - short_code -> (str) for downloading file

    HTTP methods that allows:
        - GET
    """

    permission_classes = (AllowAny,)

    def get(self, request, short_code):
        link = get_object_or_404(Link, short_code=short_code)
        file_obj = link.file

        if not file_obj:
            return Response({'detail': 'file not found'}, status=status.HTTP_404_NOT_FOUND)

        if not file_obj.can_download():
            reason = 'expired' if file_obj.is_expired() else 'limit_reached_or_inactive'
            return Response({'detail': reason}, status=status.HTTP_403_FORBIDDEN)
        try:
            with transaction.atomic():
                file_obj.increment_download_count()

                response = FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.file.name)
                return response
        except Exception as e:
            raise e
