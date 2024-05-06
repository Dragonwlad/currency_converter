from rest_framework import serializers
from currency.models import Currency, EchangeRateToUsd


class EchangeRateToUsdListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EchangeRateToUsd
        fields = ('rate', 'flowrate24', 'last_update', )


class CurrencyListSerializer(serializers.ModelSerializer):
    echangerate = serializers.SerializerMethodField()
    
    class Meta:
        model = Currency
        fields = ('name', 'name_ru', 'code', 'url_image', 'type', 'echangerate', )

    def get_echangerate(self, obj):
        """ Returns latest change rate."""

        return EchangeRateToUsdListSerializer(obj.echangerate.latest()).data


class CurrencyDetailSerializer(serializers.ModelSerializer):
    echangerate = EchangeRateToUsdListSerializer(many=True)

    class Meta:
        model = Currency
        fields = ('name', 'name_ru', 'code', 'url_image', 'type', 'echangerate', )

