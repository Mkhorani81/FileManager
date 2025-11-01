from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from account.models import User
from file.models import File
from log.models import DownloadLog


class TestDownloadLogViewSetTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            phone_number='09111111111',
            email='admin@admin.com',
            full_name='admin',
            password='root1234',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        #creating manual data
        self.user1 = User.objects.create_user(
            phone_number='09100000000',
            email='user1@test.com',
            full_name='user1',
            password='user1234',
        )

        self.file1 = File.objects.create(file='file1.txt', owner=self.user1)
        self.file2 = File.objects.create(file='file2.txt', owner=self.user1)

        DownloadLog.objects.create(user=self.user1, file=self.file1)
        DownloadLog.objects.create(user=self.user1, file=self.file2)

    def test_list_download_logs(self):
        url = reverse('log:admin-download-log-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_group_by_user(self):
        url = f"{reverse('log:admin-download-log-group-by')}?group_by=user"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(self.user1.id), response.data)
        self.assertEqual(len(response.data[str(self.user1.id)]), 2)

    def test_list_group_by_file(self):
        url = f"{reverse('log:admin-download-log-group-by')}?group_by=file"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(self.file1.id), response.data)
        self.assertIn(str(self.file2.id), response.data)

    def test_list_group_by_invalid(self):
        url = f"{reverse('log:admin-download-log-group-by')}?group_by=invalid"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid group_by value. Use "user", "file".')