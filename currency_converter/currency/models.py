from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

NAME_MAX_LENHTH = 50


class Currency(models.Model):
    '''Модель валюты.'''
    name = models.CharField(max_length=NAME_MAX_LENHTH,
                            verbose_name='Английское название')
    name_ru = models.CharField(max_length=NAME_MAX_LENHTH,
                               verbose_name='Русское название')
    code = models.CharField(max_length=3, unique=True, verbose_name='ISO код')
    url_image = models.URLField()

    class Meta:
        '''Метаданные модели.'''

        db_table = 'currency'
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self) -> str:
        '''Строчное представление объекта.'''
        return str(self.code)


class EchangeRateToUsd(models.Model):
    currency = models.ForeignKey(Currency,
                                 related_name='echangerate',
                                 on_delete=models.CASCADE)
    rate = models.FloatField(verbose_name='Он же PRICE')
    flowrate24 = models.FloatField(verbose_name='Он же CHANGE24HOUR')
    last_update = models.DateTimeField(auto_now_add=True, editable=False)
