# Generated by Django 4.2.9 on 2024-05-20 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0004_currencyechangerate_alter_currency_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyechangerate',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
