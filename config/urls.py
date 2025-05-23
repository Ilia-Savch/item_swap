from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from django.http import HttpResponse
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("ads.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("__debug__/", include(debug_toolbar.urls)),
]
