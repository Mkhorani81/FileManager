from django.test import TestCase
from rest_framework.exceptions import ValidationError

from account.models import User
from account.serializers import UserRegisterSerializer


class TestUserRegisterSerializer(TestCase):
    def setUp(self):
        User.objects.create(
            phone_number='09111111111',
            email='admin@admin.com',
            full_name='admin',
            password='root1234'
        )
        self.serializer_class = UserRegisterSerializer

    def test_clean_phone_number(self):
        data = {
            'phone_number': '09111111111',
            'email': 'dev@admin.com',
            'full_name': 'admin',
            'password': 'root1234'
        }
        ser_data = self.serializer_class(data)
        with self.assertRaises(ValidationError):
            ser_data.clean_phone_number()

    def test_clean_email(self):
        data = {
            'phone_number': '09121111111',
            'email': 'admin@admin.com',
            'full_name': 'admin',
            'password': 'root1234'
        }
        ser_data = self.serializer_class(data)
        with self.assertRaises(ValidationError):
            ser_data.clean_email()
