"""Модуль настройки OpenAPI схемы."""

from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='currency converter',
        default_version='v1',
        description='API currency converter',
        terms_of_service='https://www.google.com/policies/terms/',
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
