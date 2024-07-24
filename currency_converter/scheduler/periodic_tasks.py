"""Модуль вызова периодических задач."""
import json
import logging
import os
import datetime as dt
from django.core.files import File
from typing import List, Dict

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config.constans import CRYPTO, FIAT, TYPE_CURRENCY, FIAT_SIGN
from django.conf import settings

from currency.models.currency import Currency
from currency.models.currency_echangerate import CurrencyEchangeRate

scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)


def copy_static_image_to_currency(image_iso: str, currency: Currency) -> None:
    """
    Копирует изображение из STATIC_ROOT и сохраняет его в поле image объекта Currency.

    :param image_iso: Имя файла изображения в STATIC_ROOT.
    :param currency: Экземпляр модели Currency, в который будет сохранено изображение.
    :raises FileNotFoundError: Если изображение не найдено в STATIC_ROOT.
    """
    # Путь к файлу в STATIC_ROOT
    image_name = f'{image_iso}.png'
    static_image_path = os.path.join(settings.STATIC_ROOT, image_name)

    if os.path.exists(static_image_path):
        # Чтение изображения и сохранение его в поле image
        with open(static_image_path, 'rb') as f:
            content = File(f)
            currency.image.save(image_name, content, save=True)
    else:
        logging.warning(f"Image {image_name} not found in {settings.STATIC_ROOT}")


@scheduler.scheduled_job(
    'interval',
    minutes=settings.CRYPTO_UPDATE_INTERVAL_MINUTES,
    name='crypto_update_scheduled_job'
)
def crypto_update_exchange_rate() -> None:
    """
    Фоновая задача для запроса курса крипты и обновления данных в БД.
    В случае отсутствия валюты и курса, они создаются.
    """
    url = settings.CRYPTO_URL.format(currencies=','.join(CRYPTO.keys()))

    try:
        json_currencies_from_api = requests.get(url).text
    except Exception as error:
        logger.warning(f'Ошибка при получении курса валют: {error}')
        raise ConnectionError()

    currencies: Dict = json.loads(json_currencies_from_api).get('RAW', None)

    if currencies:
        bulk_list_change = []
        for valute, usd_currency in currencies.items():
            currency_info = usd_currency.get('USD', None)
            currency, created = Currency.objects.get_or_create(
                code=valute,
                name=CRYPTO[valute],
                url_image=currency_info['IMAGEURL'],
                type=TYPE_CURRENCY[1][0]
            )
            if created:
                CurrencyEchangeRate.objects.create(
                    currency=currency,
                    rate=currency_info['PRICE'],
                    flowrate24=currency_info['CHANGE24HOUR'],
                )
            else:
                exchanges = CurrencyEchangeRate.objects.filter(currency=currency)
                if exchanges:
                    exchange = exchanges[0]

                    exchange.rate = currency_info['PRICE']
                    exchange.flowrate24 = currency_info['CHANGE24HOUR']
                    bulk_list_change.append(exchange)

        if bulk_list_change:
            CurrencyEchangeRate.objects.bulk_update(bulk_list_change, ['rate', 'flowrate24'])

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
    Фоновая задача для запроса курса фиатов и обновления данных в БД.
    В случае отсутствия валюты и курса, они создаются.
    """
    values = ','.join(FIAT.keys())
    url = settings.FIAT_LATEST_BEACON_URL.format(api_key=settings.BEACON_API_KEY, currencies=values)
    historical_url = settings.FIAT_HISTORICAL_BEACON_URL.format(
        api_key=settings.BEACON_API_KEY,
        currencies=values,
        date=(dt.datetime.now() - dt.timedelta(days=1)).strftime('%Y-%m-%d')
    )
    try:
        json_currencies_from_api = requests.get(url).text
    except Exception as error:
        logger.warning(f'Ошибка при получении курса валют: {error}')
        raise ConnectionError()
    currencies: Dict[str, int] = json.loads(json_currencies_from_api).get('response', None).get('rates', None)

    try:
        json_currencies_from_api = requests.get(historical_url).text
    except Exception as error:
        logger.warning(f'Ошибка при получении курса валют: {error}')
        raise ConnectionError()
    yesterday_currencies: Dict[str, int] = json.loads(json_currencies_from_api).get('response', None).get('rates', None)

    if currencies and yesterday_currencies:

        bulk_list_change: List[CurrencyEchangeRate] = []
        for iso_code in currencies.keys():
            currency, created = Currency.objects.get_or_create(
                # name=FIAT[iso_code],
                code=iso_code,
                # type=TYPE_CURRENCY[0][0],
                # sign=FIAT_SIGN.get(iso_code, None)
            )
            if created:
                currency.name = FIAT[iso_code]
                currency.type = TYPE_CURRENCY[0][0]
                currency.sign = FIAT_SIGN.get(iso_code, None)
                copy_static_image_to_currency(iso_code, currency)
                CurrencyEchangeRate.objects.create(
                    currency=currency,
                    rate=currencies[iso_code],
                    flowrate24=yesterday_currencies[iso_code],
                )

            else:
                exchanges = CurrencyEchangeRate.objects.filter(currency=currency)
                if exchanges:
                    exchange = exchanges[0]
                    exchange.rate = currencies[iso_code]
                    exchange.flowrate24 = yesterday_currencies[iso_code]
                    bulk_list_change.append(exchange)

        if bulk_list_change:
            CurrencyEchangeRate.objects.bulk_update(bulk_list_change, ['rate', 'flowrate24'])
