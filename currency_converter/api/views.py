import requests
import json

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import CurrencyListSerializer, EchangeRateToUsdListSerializer, CurrencyDetailSerializer
from currency.models import Currency, EchangeRateToUsd
from currency_converter.constans import CRYPTO, FIAT, TYPE_CURRENCY, CRYPTO_URL, FIAT_URL, FIAT_FROM_CRYPTOCOMPARE



@api_view(['GET', ])
def update_or_create_crypto(request):
    '''
    Эндпоинт для запроса курса валют, парсинга и записи в БД.
    '''
    values = ''
    for key in CRYPTO.keys():
        values += key + ','
    values = values[0:len(values)-1]
    url = CRYPTO_URL.replace('ISO_LIST_VALUTE', values)
    currencyes = None
    try:
        json_currencyes_from_api = requests.get(url).text
        currencyes = json.loads(json_currencyes_from_api)
        currencyes = currencyes.get('RAW', None)
    except Exception as error:
        print('error', error)

    if not currencyes:
        return Response({'status': 'empty'}, status=status.HTTP_204_NO_CONTENT)

    bulk_list_change_to_usd = []
    for valute, usd_currency in currencyes.items():
        currency, received = Currency.objects.get_or_create(code=valute)
        currency_info = usd_currency.get('USD', None)
        if not received:
            currency.name = CRYPTO[valute]
            currency.url_image = currency_info['IMAGEURL']
            currency.type = TYPE_CURRENCY[1][0]

        current_change = EchangeRateToUsd(
            currency=currency,
            rate=currency_info['PRICE'],
            flowrate24=currency_info['CHANGE24HOUR'],
        )
        bulk_list_change_to_usd.append(current_change)

    EchangeRateToUsd.objects.bulk_create(bulk_list_change_to_usd, )

    return Response({'status': 'okk'}, status=status.HTTP_200_OK)


@api_view(['GET', ])
def update_or_create_fiat(request):
    '''
    Эндпоинт для запроса курса валют, парсинга и записи в БД.
    '''
    currencies = None
    try:
        json_currencies_from_api = requests.get(FIAT_URL).text
        currencies = json.loads(json_currencies_from_api)
        currencies = currencies.get('Valute', None)
    except Exception as error:
        print('Ошибка при получении курса валют:', error)

    if not currencies:
        return Response({'no_currencies': 'Ошибка при получении курса валют'}, status=status.HTTP_204_NO_CONTENT)

    bulk_list_exchangeable = []
    for valute in currencies.values():
        current_cur = Currency.objects.update_or_create(
            name=FIAT[valute['CharCode']],
            name_ru=valute['Name'],
            code=valute['CharCode'],
            url_image=None,
            type=TYPE_CURRENCY[0][0]
            )
        current_change = EchangeRateToUsd(
                currency=current_cur[0],
                rate=valute['Value'],
                flowrate24=abs(valute['Previous'] - valute['Value']),
            )
        bulk_list_exchangeable.append(current_change)


    return Response({'status': 'okk'}, status=status.HTTP_200_OK)


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return CurrencyListSerializer
            elif self.action == 'retrieve':
                return CurrencyDetailSerializer
        return self.serializer_class
