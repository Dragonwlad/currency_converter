from rest_framework import serializers
from currency.models import Currency, EchangeRateToUsd


class EchangeRateToUsdListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EchangeRateToUsd
        fields = ('currency', 'rate', 'flowrate24', 'last_update', )


class CurrencyListSerializer(serializers.ModelSerializer):
    echangerate = EchangeRateToUsdListSerializer(many=True)
    
    class Meta:
        model = Currency
        fields = ('name', 'name_ru', 'code', 'url_image', 'echangerate', )
