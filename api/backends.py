from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class MyExchangeProposalFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(ad_sender__user=user) | Q(ad_receiver__user=user)
        ).distinct()
