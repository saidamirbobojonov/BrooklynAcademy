from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# --- Only SUPERADMIN can see docs ---
class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to authenticated superusers.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


schema_view = get_schema_view(
    openapi.Info(
        title="BrooklynAcademy API",
        default_version="v1",
        description="API documentation for courses, users, tests, payments, etc.",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=False,  # docs are not public
    permission_classes=(IsSuperUser,),  # only authenticated superuser
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger / ReDoc (superuser-only)
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    path('', include('api.urls')),
]