from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        min_length=4
    )

    class Meta:
        model = User
        fields = ['phone_number', 'full_name', 'email', 'password']

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('Phone number already in use.')
        return phone_number

    def clean_email(self):
        email = self.data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('Email already in use.')
        return email


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        max_length=11
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        min_length=4
    )
