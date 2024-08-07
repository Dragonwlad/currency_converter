from typing import Any, Dict

from rest_framework import serializers

from currency.models.currency import Currency
from currency.models.currency_echangerate import CurrencyEchangeRate


class CurrencyEchangeRateListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CurrencyEchangeRate
        fields = ('rate', 'flowrate24', 'last_update', )


class CurrencyListSerializer(serializers.ModelSerializer):
    echangerate = serializers.SerializerMethodField()
    
    class Meta:
        model = Currency
        fields = ('name', 'name_ru', 'code', 'url_image', 'type', 'sign', 'echangerate', 'image')

    @staticmethod
    def get_echangerate(obj: Currency) -> Dict[str, Any]:
        """ Returns latest change rate."""

        return CurrencyEchangeRateListSerializer(obj.echangerate.latest()).data


class CurrencyDetailSerializer(serializers.ModelSerializer):
    echangerate = CurrencyEchangeRateListSerializer(many=True)

    class Meta:
        model = Currency
        fields = ('name', 'name_ru', 'code', 'url_image', 'type', 'sign', 'echangerate', 'image')
