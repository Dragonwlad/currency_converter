"""Модуль вызова периодических задач."""
import datetime as dt
import json
import logging
import os
from typing import Dict

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config.constans import CRYPTO, FIAT, FIAT_SIGN, TYPE_CURRENCY
from django.conf import settings
from django.core.files import File
from django.utils import timezone
from requests import Response

from currency.models.currency import Currency
from currency.models.currency_echangerate import CurrencyEchangeRate
from currency.utils import reconnect_decorator

scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)


@reconnect_decorator()
def get_request(url: str) -> Response:
    """Get response from URL."""
    return requests.get(url)


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
    name='crypto_update_scheduled_job',
    next_run_time=timezone.now(),
)
def crypto_update_exchange_rate() -> None:
    """
    Фоновая задача для запроса курса крипты и обновления данных в БД.
    В случае отсутствия валюты и курса, они создаются.
    """
    values = ','.join(CRYPTO.keys())
    url = settings.FIAT_LATEST_BEACON_URL.format(api_key=settings.BEACON_API_KEY, currencies=values)
    response = get_request(url)
    currencies: Dict = json.loads(response.text).get('RAW', None)

    if currencies:
        bulk_list_change = []
        for iso_code, usd_currency in currencies.items():
            currency_info = usd_currency.get('USD', None)
            currency, created = Currency.objects.get_or_create(
                code=iso_code,
                name=CRYPTO[iso_code],
                url_image=currency_info['IMAGEURL'],
                type=TYPE_CURRENCY[1][0]
            )
            if created:
                copy_static_image_to_currency(iso_code, currency)
                CurrencyEchangeRate.objects.create(
                    currency=currency,
                    rate=currency_info['PRICE'],
                    flowrate24=currency_info['CHANGE24HOUR'],
                )
            else:
                exchange = currency.echangerate.first()
                if exchange:
                    exchange.rate = currency_info['PRICE']
                    exchange.flowrate24 = currency_info['CHANGE24HOUR']
                    exchange.last_update = timezone.now()
                    bulk_list_change.append(exchange)

        if bulk_list_change:
            CurrencyEchangeRate.objects.bulk_update(bulk_list_change, ['rate', 'flowrate24', 'last_update'])


@scheduler.scheduled_job(
    'interval',
    minutes=settings.FIAT_UPDATE_INTERVAL_MINUTES,
    name='fiat_beacon_update_scheduled_job',
    next_run_time=timezone.now(),
)
def fiat_beacon_update_exchange_rate() -> None:
    """
    Фоновая задача для запроса курса фиатов и обновления данных в БД.
    В случае отсутствия валюты и курса, они создаются.
    """
    # settings.FIAT_LATEST_BEACON_URL
    values = ','.join(FIAT.keys())
    url = settings.FIAT_LATEST_BEACON_URL.format(api_key=settings.BEACON_API_KEY, currencies=values)
    historical_url = settings.FIAT_HISTORICAL_BEACON_URL.format(
        api_key=settings.BEACON_API_KEY,
        currencies=values,
        date=(timezone.now() - dt.timedelta(days=1)).strftime('%Y-%m-%d')
    )
    response = get_request(url)
    currencies: Dict[str, int] = json.loads(response.text).get('response', None).get('rates', None)

    yesterday_currencies: Dict[str, int] = json.loads(
        get_request(historical_url).text).get('response', None).get('rates', None)

    if currencies and yesterday_currencies:

        bulk_list_change: List[CurrencyEchangeRate] = []
        for iso_code in currencies.keys():
            rate = 1 / currencies[iso_code]
            flowrate24 = 1 / yesterday_currencies[iso_code]
            currency, created = Currency.objects.get_or_create(
                code=iso_code,
            )
            if created:
                currency.name = FIAT[iso_code]
                currency.type = TYPE_CURRENCY[0][0]
                currency.sign = FIAT_SIGN.get(iso_code, None)
                copy_static_image_to_currency(iso_code, currency)
                CurrencyEchangeRate.objects.create(
                    currency=currency,
                    rate=rate,
                    flowrate24=rate - flowrate24,
                )

            else:
                exchange = currency.echangerate.first()
                if exchange:
                    exchange.rate = rate
                    exchange.flowrate24 = rate - flowrate24
                    exchange.last_update = timezone.now()
                    bulk_list_change.append(exchange)

        if bulk_list_change:
            CurrencyEchangeRate.objects.bulk_update(
                bulk_list_change,
                ['rate', 'flowrate24', 'last_update']
            )
