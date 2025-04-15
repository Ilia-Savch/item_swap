from rest_framework import mixins
from drf_spectacular.utils import extend_schema_view, extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.core.cache import cache
from ads.models import Ad, Category, ExchangeProposal
from api.backends import MyExchangeProposalFilter
from api.filters import AdFilter, ExchangeProposalFilter
from api.mixins import ExtendedGenericViewSet
from api.pagination import AdLimitOffsetPagination
from api.permissions import IsAuthCUD, IsOwner, IsReciver
from api import serializers as serializers_
from rest_framework.permissions import IsAuthenticated

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Q

import logging


logger = logging.getLogger('item_swap')


@receiver(post_save, sender=Ad)
def clear_ads_cache_on_save(sender, instance, **kwargs):
    logger.info('Новое объявление. Чистка кэша')
    cache_key = f"ads_cache"
    cache.delete(cache_key)


@receiver(post_delete, sender=Ad)
def clear_ads_cache_on_delete(sender, instance, **kwargs):
    logger.info('Объявление удалено. Чистка кэша')
    cache_key = f"ads_cache"
    cache.delete(cache_key)


@receiver([post_save, post_delete], sender=ExchangeProposal)
def clear_exchange_cache(sender, instance, **kwargs):
    logger.info('Чистка кэша для обменов')
    user_ids = {instance.ad_sender.user.id, instance.ad_receiver.user.id}
    for user_id in user_ids:
        cache_key = f"exchange_{user_id}"
        cache.delete(cache_key)


@extend_schema_view(
    create=extend_schema(summary="Создать категорию", tags=["Категории"]),
)
class CategoryView(
    mixins.CreateModelMixin,
    ExtendedGenericViewSet,
):
    permission_classes = [
        IsAuthCUD,

    ]
    queryset = Category.objects.all()
    serializer_class = serializers_.CategorySerializer

    http_method_names = ("post",)


@extend_schema_view(
    list=extend_schema(summary='Список объявлений', tags=['Объявления']),
    create=extend_schema(summary="Создать объявление", tags=["Объявления"]),
    partial_update=extend_schema(
        summary="Изменить объявление частично", tags=["Объявления"]),
    destroy=extend_schema(summary=("Удалить объявление"), tags=["Объявления"]),
)
class AdView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    ExtendedGenericViewSet,
):
    permission_classes = [
        IsOwner,
        IsAuthCUD,

    ]
    pagination_class = AdLimitOffsetPagination
    queryset = Ad.objects.all()
    serializer_class = serializers_.AdListSerializer
    multi_serializer_class = {
        'list': serializers_.AdListSerializer,
        'create': serializers_.AdCreateSerializer,
        'partial_update': serializers_.AdUpdateSerializer,
    }
    lookup_url_kwarg = "ad_id"

    http_method_names = ("get", "post", "patch", "delete")

    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_class = AdFilter

    search_fields = (
        "title",
        "description"
    )
    ordering_fields = ('-created_at',)

    def get_queryset(self):

        cache_key = "ads_cache"

        ads_cache = cache.get(cache_key)

        if not ads_cache:
            logger.info('Кэш пуст. Кэшируем данные')
            ads_cache = Ad.objects.select_related("user", "category")
            cache.set(cache_key, ads_cache, 60*60)
        logger.info('Данные взяты из кэша')
        return ads_cache


@extend_schema_view(
    list=extend_schema(summary='Список предложений', tags=['Предложения']),
    create=extend_schema(summary="Создать предложение", tags=["Предложения"]),
    partial_update=extend_schema(
        summary="Изменить предложение частично", tags=["Предложения"]),
)
class ExchangeProposalView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    ExtendedGenericViewSet,
):
    permission_classes = [
        IsReciver,
        IsAuthenticated,
    ]
    queryset = ExchangeProposal.objects.all()
    serializer_class = serializers_.ExchangeProposalListSerializer
    multi_serializer_class = {
        'list': serializers_.ExchangeProposalListSerializer,
        'create': serializers_.ExchangeProposalCreateSerializer,
        'partial_update': serializers_.ExchangeProposalUpdateSerializer,
    }
    lookup_url_kwarg = "exchange_id"

    http_method_names = ("get", "post", "patch", )

    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyExchangeProposalFilter,
    ]

    filterset_class = ExchangeProposalFilter

    search_fields = (
        "title",
        "description"
    )

    def get_queryset(self):
        user = self.request.user

        user_id = user.id

        cache_key = f"exchange_{user_id}"

        exchange_cache = cache.get(cache_key)

        if not exchange_cache:
            logger.info('Кэш пуст. Кэшируем данные')
            exchange_cache = ExchangeProposal.objects.select_related(
                "ad_sender", "ad_receiver").filter(
                Q(ad_sender__user=user) | Q(ad_receiver__user=user)
            ).distinct()
            cache.set(cache_key, exchange_cache, 60*60)
        logger.info('Данные взяты из кэша')
        return exchange_cache
