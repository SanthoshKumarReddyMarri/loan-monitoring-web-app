from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # OpenAPI Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # Version 1 APIs
    #Versioning the API is important for maintaining backward compatibility and allowing clients to continue using older versions of the API while new features are added. By including the version number in the URL, it becomes clear which version of the API is being accessed, and it allows for easier management of different versions.
    path(
        "api/v1/health/",
        include("apps.health.urls"),
    ),



    path(
    "api/v1/auth/",
    include("apps.accounts.urls"),
),
]