from django.urls import path
from .views import (
    AdDetailView, AdListView, AdCreateView, AdUpdateView, AdDeleteView, CategoryCreateView, ExchangeProposalCreateView, ExchangeProposalStatusUpdateView, IncomingProposalsView, OutgoingProposalsView,
)

app_name = 'ads'

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('new-ad/', AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),

    path(
        'exchange-create/', ExchangeProposalCreateView.as_view(),
        name='exchange_proposal_create'),
    path('exchange-incoming/', IncomingProposalsView.as_view(),
         name='incoming_proposals'),
    path('exchange-outgoing/', OutgoingProposalsView.as_view(),
         name='outgoing_proposals'),

    path(
        'exchange-status/<int:pk>/', ExchangeProposalStatusUpdateView.as_view(),
        name='exchange_proposal_status_update'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
]
