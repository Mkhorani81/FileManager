from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DownloadLogViewSet

app_name = 'log'

router = DefaultRouter()
router.register(r'admin/download-log', DownloadLogViewSet, basename='admin-download-log')
urlpatterns = [

              ] + router.urls
