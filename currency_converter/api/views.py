import requests
import json
# from pprint import pprint
# from django.shortcuts import render
from django.db.models import Max, OuterRef, Subquery, Prefetch
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from currency.models import Currency
from api.serializers import CurrencyListSerializer, EchangeRateToUsdListSerializer
from currency.models import Currency, EchangeRateToUsd
from currency_converter.constans import ISO_TO_NAME, CURRENCY_FROM_CRYPTO, CRYPTO_URL


@api_view(['GET', ])
def currency_list(request):
    '''Эндпоинт для запроса курса валют, парсинга и записи в БД.'''
    valuete = ''
    for key in CURRENCY_FROM_CRYPTO:
        valuete += key + ','
    valuete = valuete[0:len(valuete)-1]
    url = CRYPTO_URL.replace('ISO_LIST_VALUTE', valuete)

    try:
        json_currencyes_from_api = requests.get(url).text
        currencyes = json.loads(json_currencyes_from_api)
        raw = currencyes.get('RAW', None)
        print(raw['BTC'])
    except Exception as error:
        print('error', error)

    if raw:
        bulk_list_echangeateo_usd = []
        for valute, usd_currency in raw.items():
            currency_info = usd_currency.get('USD', None)
            current_cur = Currency.objects.get_or_create(
                name=ISO_TO_NAME[valute],
                code=valute,
                url_image=currency_info['IMAGEURL'],
                )
            current_echange = EchangeRateToUsd(
                    currency=current_cur[0],
                    rate=currency_info['PRICE'],
                    flowrate24=currency_info['CHANGE24HOUR'],
                    last_update=currency_info['LASTUPDATE'],
                )
            # print(current_cur, currency_info['PRICE'], currency_info['CHANGE24HOUR'], currency_info['LASTUPDATE'],)
            bulk_list_echangeateo_usd.append(current_echange)
    bulk_list_echangeateo_usd = EchangeRateToUsd.objects.bulk_create(bulk_list_echangeateo_usd,)
    bulk_list_echangeateo_usd.save()
    # print(bulk_list_echangeateo_usd)

    return Response(
            {'error': 'okk'},
            status=status.HTTP_200_OK)


@api_view(['GET', ])
def create_currency(request):
    '''Эндпоинт для запроса валют и записи их в БД.'''
    valuete = ''
    for key in CURRENCY_FROM_CRYPTO:
        valuete += key + ','
    url = CRYPTO_URL.replace('ISO_LIST_VALUTE', valuete[0:len(valuete)-1])
    try:
        json_currencyes_from_api = requests.get(url).text
        # print(json_currencyes_from_api)
        currencyes = json.loads(json_currencyes_from_api)
        raw = currencyes.get('RAW', None)
        # print(type(raw['THB']))
        print(raw['BTC'])
    except Exception as error:
        print('error', error)

    if raw:
        bulk_list_currency = []
        for valute, usd_currency in raw.items():
            currency_info = usd_currency.get('USD', None)
            current_cur = Currency(
                    name=ISO_TO_NAME['valute'],
                    code=valute,
                    url_image=currency_info['IMAGEURL'],
                )
            bulk_list_currency.append(current_cur)
        bulk_list_currency = Currency.objects.bulk_create(bulk_list_currency)
        bulk_list_currency.save()
        return Response(
            {'Status': 'Валюты созданы'},
            status=status.HTTP_200_OK)

    return Response(
            {'Status': 'Данные не были получены'},
            status=status.HTTP_204_NO_CONTENT)



class CurrencyViewSet(viewsets.ModelViewSet):
    # queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer
    http_method_names = ('get', )


    def get_queryset(self):
        latest_exchange_rates = EchangeRateToUsd.objects.values('currency').annotate(
            latest_update=Max('last_update')
        )

        # Создаем подзапрос с помощью метода Prefetch для выбора только последнего обновления для каждой валюты
        prefetch = Prefetch('echangerate', queryset=latest_exchange_rates, to_attr='latest_echangerate')

        # Затем используем этот подзапрос в основном queryset
        queryset = Currency.objects.prefetch_related(prefetch)

        return queryset
