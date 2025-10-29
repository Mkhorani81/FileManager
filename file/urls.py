from django.urls import path
from rest_framework.routers import DefaultRouter

from file.views.client import FileUploadView, FileDownloadView
from file.views.admin import FileAdminViewSet

app_name = 'file'

router = DefaultRouter()
router.register(r'admin', FileAdminViewSet, basename='admin')

urlpatterns = [
                  path('upload/', FileUploadView.as_view(), name='file-upload'),
                  path('download/<str:short_code>/', FileDownloadView.as_view(), name='file-download'),
              ] + router.urls
