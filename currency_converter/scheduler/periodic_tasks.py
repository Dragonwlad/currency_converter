"""Модуль вызова периодических задач."""
import requests
import json

from apscheduler.schedulers.background import BackgroundScheduler
from currency_converter.constans import (
    CRYPTO, FIAT, TYPE_CURRENCY, CRYPTO_URL, FIAT_URL, FIAT_FROM_CRYPTOCOMPARE, UPDATE_INTERVAL_MINUTES
)
# import structlog

scheduler = BackgroundScheduler()
# logger = structlog.stdlib.get_logger()

@scheduler.scheduled_job('interval', seconds=10, name='crypto_update_scheduled_job')
def crypto_update_exchange_rate():
    """
    Фоновая задача для запроса курса крипты, парсинга и записи в БД.
    """
    from currency.models import Currency, EchangeRateToUsd

    print('Фоновая задача для запроса кура крипты запущена!')

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
        print('Ошибка при получении курса валют:', error)

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
                EchangeRateToUsd.objects.create(
                    currency=currency,
                    rate=currency_info['PRICE'],
                    flowrate24=currency_info['CHANGE24HOUR'],
                )
            else:
                exchanges = EchangeRateToUsd.objects.filter(currency=currency)
                if exchanges:
                    exchange = exchanges[0]

                    exchange.rate = currency_info['PRICE']
                    exchange.flowrate24 = currency_info['CHANGE24HOUR']
                    bulk_list_change.append(exchange)

        if bulk_list_change:
            EchangeRateToUsd.objects.bulk_update(bulk_list_change, ['rate', 'flowrate24'])
        print('Курс крипты обновлен и записан в БД!')
        # logger.info('Курс крипты обновлен и записан в БД!')
    # logger.info('crypto_update_scheduled_job_finish!')
    print('Курс крипты обновлен и записан в БД!')


@scheduler.scheduled_job('interval', seconds=10, name='fiat_update_scheduled_job')
def fiat_update_exchange_rate():
    """
    Фоновая задача для запроса курса фиатов, парсинга и записи в БД.
    """
    from currency.models import Currency, EchangeRateToUsd

    print('Фоновая задача для запроса кура фиата запущена!')
    currencyes = None
    try:
        json_currencies_from_api = requests.get(FIAT_URL).text
        currencyes = json.loads(json_currencies_from_api)
        currencyes = currencyes.get('Valute', None)
    except Exception as error:
        print('Ошибка при получении курса валют:', error)

    if currencyes:

        bulk_list_exchangeable = []
        for valute in currencyes.values():
            currency, received = Currency.objects.get_or_create(code=valute)
            if not received:
                currency.name = FIAT[valute['CharCode']]
                currency.name_ru = valute['Name']
                currency.code = valute['CharCode']
                currency.type = TYPE_CURRENCY[0][0]

            current_change = EchangeRateToUsd(
                    currency=currency,
                    rate=valute['Value'],
                    flowrate24=abs(valute['Previous'] - valute['Value']),
                )
            bulk_list_exchangeable.append(current_change)

        EchangeRateToUsd.objects.bulk_update(bulk_list_exchangeable, fields=['rate', 'flowrate24'])
        print('Курс фиатов обновлен и записан в БД!')

    print('fiat_update_scheduled_job_finish!')
