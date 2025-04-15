from api.spectacular.urls import urlpatterns as doc_urls
from django.urls import include, path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from api.views import AdView, ExchangeProposalView, CategoryView


router = DefaultRouter()
router.register(r"ads", AdView, basename="ads")
router.register(r"categories", CategoryView, basename="categories")
router.register(r"exchanges", ExchangeProposalView, basename="exchanges")

app_name = 'api'

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.jwt")),
]

urlpatterns += doc_urls
