from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('currencies', views.CurrencyViewSet, basename='currencies')

app_name = 'api'

urlpatterns = [
    path('<slug:price_id>/buy/', views.currency_list),
    path('', include(router.urls), )

]
