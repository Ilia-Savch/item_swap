import pytest
from django.test import TestCase
from django.urls import reverse
from ads.models import Category,  Ad, ExchangeProposal
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
import logging
from django.test import Client
logger = logging.getLogger("item_swap")


@pytest.mark.django_db
class TestAdListView:

    def test_ad_list_view(self, client,):
        url = reverse('ads:ad_list')
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestAdCreateView:

    def test_ad_create_view(self, client, user, category, uploaded_file):
        client.login(username='testuser', password='testpassword')
        url = reverse('ads:ad_create')
        data = {
            "title": "Smartphone",
            "description": "Latest model",
            "category": category.id,
            "condition": "new",
            "image_url": uploaded_file,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Ad.objects.count() == 1


@pytest.mark.django_db
class TestAdUpdateView:

    def test_ad_update_view(self, client, user, ad, category):
        client.login(username='testuser', password='testpassword')
        url = reverse('ads:ad_update', kwargs={'pk': ad.pk})
        logger.info(f'URL: {url}')

        data = {
            'title': 'Updated Ad',
            'description': 'Updated description',
            'category': category.id,
            'condition': 'new',
        }
        response = client.post(url, data)
        ad.refresh_from_db()
        assert response.status_code == 302
        assert ad.title == 'Updated Ad'


@pytest.mark.django_db
class TestAdDeleteView:

    def test_ad_delete_view(self, client, user, ad):
        client.login(username='testuser', password='testpassword')
        url = reverse('ads:ad_delete', kwargs={'pk': ad.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert Ad.objects.count() == 0


@pytest.mark.django_db
class TestAdDeleteView:

    def test_ad_delete_view(self, client, user, ad):
        client.login(username='testuser', password='testpassword')
        url = reverse('ads:ad_delete', kwargs={'pk': ad.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert Ad.objects.count() == 0


@pytest.mark.django_db
class TestExchangeProposalCreateView:

    def test_exchange_proposal_create_view(self, client, user, ad, category):
        user_receiver = User.objects.create_user(
            username="testuser2", password="testpassword")

        ad_receiver = Ad.objects.create(
            title="Test Ad",
            description="Test Description",
            category=category,
            user=user_receiver,
            condition="new"
        )

        client1 = Client()
        client2 = Client()

        client1.login(username='testuser', password='testpassword')
        client2.login(username='testuser2', password='testpassword')

        url = reverse('ads:exchange_proposal_create')

        data = {
            'ad_sender': ad.id,
            'ad_receiver': ad_receiver.id,
            'status': 'pending'
        }

        response = client1.post(url, data)
        assert response.status_code == 302
        assert ExchangeProposal.objects.count() == 1


@pytest.mark.django_db
class TestIncomingProposalsView:

    def test_incoming_proposals_view(self, client, user,):
        client.login(username='testuser', password='testpassword')
        url = reverse('ads:incoming_proposals')
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestOutgoingProposalsView:

    def test_outgoing_proposals_view(self, client, user, ):
        client.login(username='testuser', password='testpassword')
        url = reverse('ads:outgoing_proposals')
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestExchangeProposalStatusUpdateView:

    def test_exchange_proposal_status_update_view(self, client, user, exchange_proposal):
        client.login(username='testuser2', password='testpassword')
        url = reverse(
            'ads:exchange_proposal_status_update',
            kwargs={'pk': exchange_proposal.id})
        data = {'status': 'accepted'}
        response = client.post(url, data)
        exchange_proposal.refresh_from_db()
        assert response.status_code == 302
        assert exchange_proposal.status == 'accepted'


@pytest.mark.django_db
class TestCategoryCreateView:

    def test_category_create_view(self, client, user):
        client.login(username='testuser', password='testpassword')
        url = reverse('ads:category_create')
        data = {'name': 'New Category'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert Category.objects.count() == 1
