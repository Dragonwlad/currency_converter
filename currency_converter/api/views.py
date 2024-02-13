from django.shortcuts import render
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from currency.models import Currency
from api.serializers import CurrencyListSerializer, EchangeRateToUsdListSerializer

'''
JSON =  {
    lastUpdate: 178249273,
    baseCode: "USD",
    coins: [
        {
            "code": "BTC",
            "name": "Bitcoin",
            "nameRU": "",
            "rate": 378483.234,
            "flowRate24": -0.22,
            "urlImage": "/media/..."
        }
    ]
}
JSON =  {

            "code": "BTC",
            "name": "Bitcoin",
            "nameRU": "",
            "urlImage": "/media/...",
            'baseCode': "USD",
            updates: [
                {
                    "rate": 378483.234,
                    "flowRate24": -0.22,
                    "last_update": "",
                }
        }
'''


@api_view(['GET', ])
def currency_list(request):
    return Response(
            {'error': 'OKK'},
            status=status.HTTP_200_OK)


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer
    http_method_names = ('get', )


    def get_queryset(self):
        currency = self.request.body
        print(currency)
        return super().get_queryset()
