from django.urls import path
from file.views.client import FileUploadView, FileDownloadView

app_name = 'file'

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('download/<str:short_code>/', FileDownloadView.as_view(), name='file-download'),
]
