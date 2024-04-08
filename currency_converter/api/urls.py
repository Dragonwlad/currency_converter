from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('currencies', views.CurrencyViewSet, basename='currencies')

app_name = 'api'

urlpatterns = [
    path('get-currencies/', views.currency_list),
    path('create-currencies/', views.create_currency),
    path('', include(router.urls), )

]
