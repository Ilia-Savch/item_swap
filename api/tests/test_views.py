import pytest

from ads.models import Ad, Category
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestAdView:

    def test_create(self, auth_client, uploaded_file, ads_url, category):
        data = {
            "title": "Smartphone",
            "description": "Latest model",
            "category": category.id,
            "condition": "new",
            "image_url": uploaded_file,
        }

        response = auth_client.post(ads_url, data, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert Ad.objects.filter(title="Smartphone").exists()

    def test_list(self, auth_client, ads_url):
        response = auth_client.get(ads_url)
        assert response.status_code == 200

    def test_update(self, ads_url, uploaded_file, auth_client, user, category):
        category_patсh = Category.objects.create(name="New Patch")

        ad_ = Ad.objects.create(
            title="Smartphone Patch",
            description="Latest model Patch",
            category=category_patсh,
            condition="poor",
            image_url=uploaded_file,
            user=user
        )

        data = {
            "title": "Smartphone",
            "description": "Latest model",
            "category": category.id,
            "condition": "new",
        }

        response = auth_client.patch(
            ads_url+f"{ad_.id}/", data, format="multipart")
        assert response.status_code == 200

    def test_delete(self, ads_url, user, auth_client):
        ad_ = Ad.objects.create(
            title="Smartphone Patch",
            description="Latest model Patch",
            condition="poor",
            user=user
        )
        assert Ad.objects.count() == 1

        response = auth_client.delete(ads_url + f"{ad_.id}/")

        assert response.status_code == 204

        assert Ad.objects.count() == 0
