from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('currencies', views.CurrencyViewSet, basename='currencies')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls), )
]
