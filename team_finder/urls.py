"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from projects.web_views import ProjectListView

urlpatterns = [
    path("", ProjectListView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("projects/", include("projects.urls")),
    path("users/", include("users.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/v1/", include("projects.api_urls")),
]
