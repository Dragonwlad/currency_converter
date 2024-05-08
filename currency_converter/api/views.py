import logging

from api.serializers import CurrencyDetailSerializer, CurrencyListSerializer
from currency.models.currency import Currency
from rest_framework import mixins, viewsets


class CurrencyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """Вьюсет для получения списка криптовалют."""
    queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return CurrencyListSerializer
            elif self.action == 'retrieve':
                return CurrencyDetailSerializer
        return self.serializer_class
