from django.urls import path
from file.views.client import FileUploadView

app_name = 'file'

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
