from django.contrib.auth import get_user_model
from django.db import models

from currency.models.currency import Currency

User = get_user_model()


class CurrencyEchangeRate(models.Model):
    currency = models.ForeignKey(Currency,
                                 related_name='echangerate',
                                 on_delete=models.CASCADE
                                 )
    rate = models.FloatField(verbose_name='Он же PRICE', null=True)
    flowrate24 = models.FloatField(verbose_name='Он же CHANGE24HOUR', null=True)
    last_update = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы валют'
        get_latest_by = 'last_update'
