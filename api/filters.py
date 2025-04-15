import django_filters
from ads.models import Ad, ExchangeProposal


class AdFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__name', lookup_expr='iexact')
    condition = django_filters.ChoiceFilter(
        choices=Ad.CONDITION_CHOICES, lookup_expr='iexact')

    class Meta:
        model = Ad
        fields = ['category', 'condition']


class ExchangeProposalFilter(django_filters.FilterSet):

    is_sender = django_filters.filters.BooleanFilter(
        method='is_sender_filter', label='Я отправил')
    is_receiver = django_filters.BooleanFilter(
        method='is_receiver_filter', label='Мне отправили')
    status = django_filters.ChoiceFilter(
        choices=ExchangeProposal.STATUS_CHOICES, lookup_expr='iexact')

    class Meta:
        model = ExchangeProposal
        fields = ["is_sender", "is_receiver", 'status',]

    def is_sender_filter(self, queryset, name, value):
        if value:
            return queryset.filter(ad_sender__user=self.request.user)
        return queryset

    def is_receiver_filter(self, queryset, name, value):
        if value:
            return queryset.filter(ad_receiver__user=self.request.user)
        return queryset
