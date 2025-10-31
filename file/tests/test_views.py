from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from account.models import User
from file.views.admin import FileAdminViewSet
from file.views.client import FileUploadView, FileDownloadView


class TestFileUploadView(APITestCase):
    """
    This test is for testing the file upload view on 3 scenarios:
        - un authenticated user -> (401 status code)
        - authenticated user with valid data -> (201 status code)
        - authenticated user with invalid data -> (400 status code)
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(phone_number='09111111111', email='admin@admin.com', full_name='admin',
                                             password='root1234')
        self.url = reverse('file:file-upload')

    def test_unauthenticated_user(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('file.views.client.FileUploadView.post')
    def test_authenticated_user_valid_data(self, mock_post):
        self.client.force_authenticate(user=self.user)

        mock_post.return_value = Response(
            data={
                'link': 'testLink1234',
                'file_id': 'testID1234'
            },
            status=status.HTTP_201_CREATED,
        )

        test_file = SimpleUploadedFile('test.txt', b'test content', content_type='text/plain')
        response = self.client.post(self.url, {'file': test_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['link'], 'testLink1234')
        self.assertEqual(response.data['file_id'], 'testID1234')
        mock_post.assert_called_once()

    @patch('file.views.client.FileUploadView.post')
    def test_authenticated_user_invalid_data(self, mock_post):
        self.client.force_authenticate(user=self.user)

        mock_post.return_value = Response(
            data={
                'file': ['This field is required or invalid.']
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.post(self.url, {}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', response.data)
        mock_post.assert_called_once()
