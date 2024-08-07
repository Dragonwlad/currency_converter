# Generated by Django 4.2.9 on 2024-07-10 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='image',
            field=models.ImageField(default=False, upload_to='currency/images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currency',
            name='sign',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
