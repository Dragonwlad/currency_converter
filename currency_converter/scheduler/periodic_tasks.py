"""Модуль вызова периодических задач."""
import json
import logging
import datetime as dt
from typing import List, Dict

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config.constans import CRYPTO, FIAT, TYPE_CURRENCY
from django.conf import settings

scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)


# @scheduler.scheduled_job('interval', minutes=CRYPTO_UPDATE_INTERVAL_MINUTES, name='crypto_update_scheduled_job')
# def crypto_update_exchange_rate() -> None:
#     """
#     Фоновая задача для запроса курса крипты и обновления данных в БД. В случае отсутствия валюты и курса, они создаются.
#     """
#     from currency.models.currency import Currency
#     from currency.models.currency_echangerate import CurrencyEchangeRate
#     logger.info('Запущена периодическая задача для запроса курса крипты.')
#
#     values = ''
#     for key in CRYPTO.keys():
#         values += key + ','
#     values = values[0:len(values)-1]
#     url = setting.CRYPTO_URL.replace('ISO_LIST_VALUTE', values)
#     currencyes = None
#
#     try:
#         json_currencyes_from_api = requests.get(url).text
#         currencyes = json.loads(json_currencyes_from_api)
#         currencyes = currencyes.get('RAW', None)
#     except Exception as error:
#         logger.warning(f'Ошибка при получении курса валют: {error}')
#
#     if currencyes:
#         bulk_list_change = []
#         for valute, usd_currency in currencyes.items():
#             currency_info = usd_currency.get('USD', None)
#             currency, created = Currency.objects.get_or_create(
#                 code=valute,
#                 name=CRYPTO[valute],
#                 url_image=currency_info['IMAGEURL'],
#                 type=TYPE_CURRENCY[1][0]
#             )
#             if created:
#                 CurrencyEchangeRate.objects.create(
#                     currency=currency,
#                     rate=currency_info['PRICE'],
#                     flowrate24=currency_info['CHANGE24HOUR'],
#                 )
#             else:
#                 exchanges = CurrencyEchangeRate.objects.filter(currency=currency)
#                 if exchanges:
#                     exchange = exchanges[0]
#
#                     exchange.rate = currency_info['PRICE']
#                     exchange.flowrate24 = currency_info['CHANGE24HOUR']
#                     bulk_list_change.append(exchange)
#
#         if bulk_list_change:
#             CurrencyEchangeRate.objects.bulk_update(bulk_list_change, ['rate', 'flowrate24'])
#         print('Курс крипты обновлен и записан в БД!')
#
#
# @scheduler.scheduled_job('interval', minutes=FIAT_UPDATE_INTERVAL_MINUTES, name='fiat_CB_update_scheduled_job')
# def fiat_update_exchange_rate() -> None:
#     """
#     Фоновая задача для запроса курса фиатов и обновления данных в БД. В случае отсутствия валюты и курса, они создаются.
#     """
#     from currency.models.currency import Currency
#     from currency.models.currency_echangerate import CurrencyEchangeRate
#
#     logger.info('Запущена периодическая задача для запроса курса фиата.')
#     try:
#         json_currencies_from_api = requests.get(settings.FIAT_URL).text
#         currencyes = json.loads(json_currencies_from_api)
#         currencyes = currencyes.get('Valute', None)
#     except Exception as error:
#         logger.warning(f'Ошибка при получении курса валют: {error}')
#         raise ConnectionError()
#
#     if currencyes:
#
#         bulk_list_change = []
#         for valute in currencyes.values():
#             currency, created = Currency.objects.get_or_create(
#                 name=FIAT[valute['CharCode']],
#                 name_ru=valute['Name'],
#                 code=valute['CharCode'],
#                 type=TYPE_CURRENCY[0][0]
#
#             )
#             if created:
#                 CurrencyEchangeRate.objects.create(
#                     currency=currency,
#                     rate=valute['Value'],
#                     flowrate24=abs(valute['Previous'] - valute['Value']),
#                 )
#
#             else:
#                 exchanges = CurrencyEchangeRate.objects.filter(currency=currency)
#                 if exchanges:
#                     exchange = exchanges[0]
#                     exchange.rate = valute['Value']
#                     exchange.flowrate24 = abs(valute['Previous'] - valute['Value'])
#                     bulk_list_change.append(exchange)
#
#         if bulk_list_change:
#             CurrencyEchangeRate.objects.bulk_update(bulk_list_change, ['rate', 'flowrate24'])
#
#     print('Курс фиатов обновлен и записан в БД!')


@scheduler.scheduled_job(
    'interval',
    minutes=settings.FIAT_UPDATE_INTERVAL_MINUTES,
    name='fiat_beacon_update_scheduled_job'
)
def fiat_beacon_update_exchange_rate() -> None:
    """
    Фоновая задача для запроса курса фиатов и обновления данных в БД. В случае отсутствия валюты и курса, они создаются.
    """
    from currency.models.currency import Currency
    from currency.models.currency_echangerate import CurrencyEchangeRate

    logger.info('Запущена периодическая задача для запроса курса фиата.')
    values = ','.join(FIAT.keys())
    url = settings.FIAT_LATEST_BEACON_URL.format(api_key=settings.BEACON_API_KEY, currencies=values)
    historical_url = settings.FIAT_HISTORICAL_BEACON_URL.format(
        api_key=settings.BEACON_API_KEY,
        currencies=values,
        date=dt.datetime.now().strftime('%Y-%m-%d')
    )
    try:
        json_currencies_from_api = requests.get(url).text
    except Exception as error:
        logger.warning(f'Ошибка при получении курса валют: {error}')
        raise ConnectionError()
    currencyes: Dict[str, int] = json.loads(json_currencies_from_api).get('response', None).get('rates', None)

    try:
        json_currencies_from_api = requests.get(historical_url).text
    except Exception as error:
        logger.warning(f'Ошибка при получении курса валют: {error}')
        raise ConnectionError()
    yesterday_currencyes: Dict[str, int] = json.loads(json_currencies_from_api).get('response', None).get('rates', None)

    if currencyes and yesterday_currencyes:

        bulk_list_change: List[CurrencyEchangeRate] = []
        for iso_code in currencyes.keys():
            currency, created = Currency.objects.get_or_create(
                name=FIAT[iso_code],
                # name_ru=valute['Name'],
                code=iso_code,
                type=TYPE_CURRENCY[0][0]

            )
            if created:
                CurrencyEchangeRate.objects.create(
                    currency=currency,
                    rate=value,
                    flowrate24=abs(valute['Previous'] - valute['Value']),
                )

            else:
                exchanges = CurrencyEchangeRate.objects.filter(currency=currency)
                if exchanges:
                    exchange = exchanges[0]
                    exchange.rate = valute['Value']
                    exchange.flowrate24 = abs(valute['Previous'] - valute['Value'])
                    bulk_list_change.append(exchange)

        if bulk_list_change:
            CurrencyEchangeRate.objects.bulk_update(bulk_list_change, ['rate', 'flowrate24'])

    logger.info('Курс фиатов обновлен и записан в БД!')


if __name__ == '__main__':
    print('hellp')
