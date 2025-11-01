from unittest.mock import patch, MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APITestCase, APIClient

from account.models import User


class TestUserRegisterView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('account:register')

    @patch('account.views.User')
    @patch('account.views.UserRegisterSerializer')
    def test_register_user_valid_serializer(self, mock_serializer_class, mock_user):
        request_data = {
            'phone_number': '09111111111',
            'email': 'test@admin.com',
            'full_name': 'test user',
            'password': 'root-test'
        }
        response_data = {
            'phone_number': '09111111111',
            'email': 'test@admin.com',
            'full_name': 'test user',
        }
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = request_data
        mock_serializer.data = response_data
        mock_serializer_class.return_value = mock_serializer

        response = self.client.post(self.url, data=request_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data, response_data)
        mock_user.objects.create_user.assert_called_once_with(
            phone_number='09111111111',
            email='test@admin.com',
            full_name='test user',
            password='root-test'
        )

    @patch('account.views.UserRegisterSerializer')
    def test_register_user_invalid_serializer(self, mock_serializer_class):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'phone_number': ['This field is required.']}
        mock_serializer_class.return_value = mock_serializer

        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
        self.assertIn('This field is required.', str(response.data['phone_number']))
