import requests
import json
from pprint import pprint
from django.shortcuts import render
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from currency.models import Currency
from api.serializers import CurrencyListSerializer, EchangeRateToUsdListSerializer
from currency.models import Currency, EchangeRateToUsd

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

currency_from_crypto = ('THB', 'SOL', 'TRY', 'NZD', 'SGD', 'CZK', 'ARB', 'HUF',
                        'HKD', 'AVAX', 'QAR', 'UZS', 'BNB', 'SUI', 'EGP',
                        'LTC', 'RON', 'MDL', 'CAD', 'XRP', 'PEOPLE', 'JPY',
                        'SEI', 'ENS', 'RSD', 'DOGE', 'BCH', 'PLN',
                        'TUSD', 'BSV', 'NOK', 'ETC', 'AMD', 'AUD',
                        'ICP', 'TJS', 'ETH', 'XDR', 'GBP', 'USD',
                        'EUR', 'FDUSD', 'AED', 'BGN', 'CHF', 'UAH',
                        'TIA', 'LINK', 'WBTC', 'KZT', 'BYN', 'DOT',
                        'SHIB', 'BONK', 'INJ', 'MATIC', 'DKK', 'FIL',
                        'AZN', 'KGS', 'KRW', 'USDC', 'INR', 'LDO', 'ZAR',
                        'VND', 'BTC', 'OP', 'USDT', 'MANTLE', 'SEK', 'TRX',
                        'STX', 'CNY', 'IDR', 'TMT', 'GMT', 'RUB', 'BRL',
                        'GEL', 'APT', 'ADA', 'WSB', 'NEAR'
                        )

names = {
    "RUB": "Russian Ruble",
    "AUD": "Australian Dollar",
    "AZN": "Azerbaijani Manat",
    "GBP": "British Pound Sterling",
    "AMD": "Armenian Dram",
    "BYN": "Belarusian Ruble",
    "BGN": "Bulgarian Lev",
    "BRL": "Brazilian Real",
    "HUF": "Hungarian Forint",
    "VND": "Vietnamese Dong",
    "HKD": "Hong Kong Dollar",
    "GEL": "Georgian Lari",
    "DKK": "Danish Krone",
    "AED": "UAE Dirham",
    "USD": "United States Dollar",
    "EUR": "Euro",
    "EGP": "Egyptian Pound",
    "INR": "Indian Rupee",
    "IDR": "Indonesian Rupiah",
    "KZT": "Kazakhstani Tenge",
    "CAD": "Canadian Dollar",
    "QAR": "Qatari Rial",
    "KGS": "Kyrgystani Som",
    "CNY": "Chinese Yuan",
    "MDL": "Moldovan leu",
    "NZD": "New Zealand Dollar",
    "NOK": "Norwegian Krone",
    "PLN": "Polish Zloty",
    "RON": "Romanian Leu",
    "XDR": "Special Drawing Rights",
    "SGD": "Singapore dollar",
    "TJS": "Tajikistani somoni",
    "THB": "Thai baht",
    "TRY": "Turkish Lira",
    "TMT": "Turkmenistani Manat",
    "UZS": "Uzbekistan Som",
    "UAH": "Ukranian Hryvnia",
    "CZK": "Czech Koruna",
    "SEK": "Swedish Krona",
    "CHF": "Swiss Franc",
    "RSD": "Serbian Dinar",
    "ZAR": "South African Rand",
    "KRW": "Korean Won",
    "JPY": "Japanese Yen",
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "XRP": "XRP",
    "ARB": "Arbitrum",
    "USDC": "USD Coin",
    "FDUSD": "First Digital USD",
    "DOGE": "Dogecoin",
    "USDT": "Tether",
    "AVAX": "Avalanche",
    "OP": "Optimism",
    "ADA": "Cardano",
    "BNB": "Binance Coin",
    "MATIC": "Polygon",
    "LINK": "Chainlink",
    "WSB": "WallStreetBets DApp",
    "BONK": "Bonk",
    "LTC": "Litecoin",
    "ETC": "Ethereum Classic",
    "LDO": "Lido DAO",
    "TIA": "Celestia",
    "FIL": "FileCoin",
    "MANTLE": "Mantle",
    "SEI": "Sei",
    "INJ": "Injective",
    "SHIB": "Shiba Inu",
    "BCH": "Bitcoin Cash",
    "ICP": "Internet Computer",
    "STX": "Stacks",
    "DOT": "Polkadot",
    "TRX": "TRON",
    "NEAR": "Near",
    "PEOPLE": "ConstitutionDAO",
    "ENS": "Ethereum Name Service",
    "APT": "Aptos",
    "SUI": "Sui",
    "TUSD": "True USD",
    "GMT": "STEPN",
    "BSV": "Bitcoin SV",
    "WBTC": "Wrapped Bitcoin",
    }


valuete = ''

for key in currency_from_crypto:
    valuete += key + ','
valuete = valuete[0:len(valuete)-1]
# print(valuete)

url = f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={valuete}&tsyms=USD'


@api_view(['GET', ])
def currency_list(request):
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
        bulk_list_echangeateo_usd = []
        for valute, usd_currency in raw.items():
            # Создание валюты
            # current_cur = Currency(
            #         name=currency_info['FROMSYMBOL'],
            #         code=valute,
            #         url_image=currency_info['IMAGEURL'],
            #     )

            currency_info = usd_currency.get('USD', None)
            current_cur = Currency.objects.get_or_create(
                name=currency_info['FROMSYMBOL'],
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

            # bulk_list_currency.append(current_cur)
            bulk_list_echangeateo_usd.append(current_echange)
    # bulk_list_currency = Currency.objects.bulk_create(bulk_list_currency)
    bulk_list_echangeateo_usd = EchangeRateToUsd.objects.bulk_create(bulk_list_echangeateo_usd,)
    # bulk_list_currency.save()
    # bulk_list_echangeateo_usd.save()
    # print(bulk_list_currency)
    # print(bulk_list_echangeateo_usd)

    return Response(
            {'error': 'okk'},
            status=status.HTTP_200_OK)


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer
    http_method_names = ('get', )


    def get_queryset(self):
        latest_exchange_rates = EchangeRateToUsd.objects.values('currency').annotate(
            max_last_update=Max('last_update')
        )
        return super().get_queryset()
