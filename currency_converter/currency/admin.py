from currency.models.currency import Currency
from currency.models.currency_echangerate import CurrencyEchangeRate
from django.contrib import admin


class CurrencyEchangeRateInLine(admin.TabularInline):
    model = CurrencyEchangeRate
    extra = 1


@admin.register(Currency)
class Currency(admin.ModelAdmin):
    inlines = [CurrencyEchangeRateInLine, ]


admin.site.register(CurrencyEchangeRate)
