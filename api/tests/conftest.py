from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123',
    )


@pytest.fixture
def user_receiver():
    return User.objects.create_user(
        username='testuser2',
        email='testuser2@example.com',
        password='testpassword123',

    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_client_receiver(user_receiver):
    client = APIClient()
    client.force_authenticate(user=user_receiver)
    return client


@pytest.fixture
def ads_url():
    return "/api/ads/"
