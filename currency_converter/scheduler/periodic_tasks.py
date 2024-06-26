"""Модуль вызова периодических задач."""
import json
import logging

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config.constans import (
    CRYPTO, CRYPTO_UPDATE_INTERVAL_MINUTES, CRYPTO_URL, FIAT, FIAT_FROM_CRYPTOCOMPARE, FIAT_UPDATE_INTERVAL_MINUTES,
    FIAT_URL, TYPE_CURRENCY,
)

scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)


@scheduler.scheduled_job('interval', minutes=CRYPTO_UPDATE_INTERVAL_MINUTES, name='crypto_update_scheduled_job')
def crypto_update_exchange_rate() -> None:
    """
    Фоновая задача для запроса курса крипты и обновления данных в БД. В случае отсутствия валюты и курса, они создаются.
    """
    from currency.models.currency import Currency
    from currency.models.currency_echangerate import CurrencyEchangeRate
    logger.info('Запущена периодическая задача для запроса курса крипты.')

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
        logger.warning(f'Ошибка при получении курса валют: {error}')

    if currencyes:
        bulk_list_change = []
        for valute, usd_currency in currencyes.items():
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
        print('Курс крипты обновлен и записан в БД!')


@scheduler.scheduled_job('interval', minutes=FIAT_UPDATE_INTERVAL_MINUTES, name='fiat_update_scheduled_job')
def fiat_update_exchange_rate() -> None:
    """
    Фоновая задача для запроса курса фиатов и обновления данных в БД. В случае отсутствия валюты и курса, они создаются.
    """
    from currency.models.currency import Currency
    from currency.models.currency_echangerate import CurrencyEchangeRate

    logger.info('Запущена периодическая задача для запроса курса фиата.')
    currencyes = None
    try:
        json_currencies_from_api = requests.get(FIAT_URL).text
        currencyes = json.loads(json_currencies_from_api)
        currencyes = currencyes.get('Valute', None)
    except Exception as error:
        logger.warning(f'Ошибка при получении курса валют: {error}')

    if currencyes:

        bulk_list_change = []
        for valute in currencyes.values():
            currency, created = Currency.objects.get_or_create(
                name=FIAT[valute['CharCode']],
                name_ru=valute['Name'],
                code=valute['CharCode'],
                type=TYPE_CURRENCY[0][0]

            )
            if created:
                CurrencyEchangeRate.objects.create(
                    currency=currency,
                    rate=valute['Value'],
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

    print('Курс фиатов обновлен и записан в БД!')
