from django.contrib import admin

from currency.models import Currency, EchangeRateToUsd


class EchangeRateToUsdInLine(admin.TabularInline):
    model = EchangeRateToUsd
    extra = 1


@admin.register(Currency)
class Currency(admin.ModelAdmin):
    inlines = [EchangeRateToUsdInLine, ]


admin.site.register(EchangeRateToUsd)