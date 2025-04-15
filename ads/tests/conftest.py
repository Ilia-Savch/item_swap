
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category, ExchangeProposal
from django.contrib.auth.models import User

from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def user_receiver():
    return User.objects.create_user(username="testuser2", password="testpassword")


@pytest.fixture
def ad(user, category):
    return Ad.objects.create(
        title="Test Ad",
        description="Test Description",
        category=category,
        user=user
    )


@pytest.fixture
def ad_receiver(user, category, user_receiver):
    return Ad.objects.create(
        title="Test Ad",
        description="Test Description",
        category=category,
        user=user_receiver
    )


@pytest.fixture
def exchange_proposal(ad, ad_receiver):
    return ExchangeProposal.objects.create(
        ad_sender=ad,
        ad_receiver=ad_receiver,
        status="pending"
    )
