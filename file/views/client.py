from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from file.models import Link
from file.serializers.clinet import FileUploadSerializer


class FileUploadView(APIView):
    """
    This view used to upload new file,
    The parameters:
        - file (File field with specific format could be customized in config file)
        - max_downloads -> (Integer field)
        - expires_at -> (Datetime field)

        other parameters fill out automatically
    """

    serializer_class = FileUploadSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            file_obj = serializer.save()
            link = Link.objects.generate_download_link(file_obj)
            response = {
                'link': link.short_code,
                'file_id': file_obj.id,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
