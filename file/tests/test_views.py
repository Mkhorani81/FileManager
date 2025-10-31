from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, MagicMock
from django.urls import reverse

from account.models import User
from file.views.admin import FileAdminViewSet
from file.views.client import FileUploadView, FileDownloadView


class TestFileUploadView(APITestCase):
    """
    This test is for testing the file upload view
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(phone_number='09111111111', email='admin@admin.com', full_name='admin',
                                             password='root1234')
        self.url = reverse('file:file-upload')

    def test_unauthenticated_user(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_valid_data(self):
        pass

    def test_authenticated_user_invalid_data(self):
        pass