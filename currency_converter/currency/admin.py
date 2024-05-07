from django.contrib import admin

from currency.models.currency import Currency
from currency.models.currency_echangerate import CurrencyEchangeRate


class CurrencyEchangeRateInLine(admin.TabularInline):
    model = CurrencyEchangeRate
    extra = 1


@admin.register(Currency)
class Currency(admin.ModelAdmin):
    inlines = [CurrencyEchangeRateInLine, ]


admin.site.register(CurrencyEchangeRate)
