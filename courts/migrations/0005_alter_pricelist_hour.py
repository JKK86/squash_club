# Generated by Django 3.2.4 on 2021-07-12 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0004_auto_20210712_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelist',
            name='hour',
            field=models.IntegerField(blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)], null=True, verbose_name='Godzina'),
        ),
    ]
