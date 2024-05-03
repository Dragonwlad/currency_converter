from django.contrib.auth import get_user_model
from django.db import models

from currency_converter.constans import TYPE_CURRENCY

User = get_user_model()

NAME_MAX_LENGTH = 50

ISO_CODE_LENGTH = 3


class Currency(models.Model):
    """Модель валюты."""
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Английское название')
    name_ru = models.CharField(max_length=NAME_MAX_LENGTH,
                               verbose_name='Русское название')
    code = models.CharField(max_length=ISO_CODE_LENGTH, unique=True, verbose_name='ISO код')
    type = models.CharField(max_length=NAME_MAX_LENGTH,choices=TYPE_CURRENCY)
    url_image = models.URLField(verbose_name='Ссылка на изображение', null=True, blank=True)

    class Meta:
        """Метаданные модели."""

        db_table = 'currency'
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self) -> str:
        """Строчное представление объекта."""
        return str(self.code)


class EchangeRateToUsd(models.Model):
    currency = models.ForeignKey(Currency,
                                 related_name='echangerate',
                                 on_delete=models.CASCADE
                                 )
    rate = models.FloatField(verbose_name='Он же PRICE', null=True)
    flowrate24 = models.FloatField(verbose_name='Он же CHANGE24HOUR', null=True)
    last_update = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы валют'
        get_latest_by = 'last_update'
