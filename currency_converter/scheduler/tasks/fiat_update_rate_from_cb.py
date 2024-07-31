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
