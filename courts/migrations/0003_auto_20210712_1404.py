# Generated by Django 3.2.4 on 2021-07-12 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0002_auto_20210707_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='number',
            field=models.PositiveIntegerField(unique=True, verbose_name='Numer kortu'),
        ),
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekend', models.BooleanField(default=False)),
                ('hour', models.CharField(choices=[('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('11', 11), ('12', 12), ('13', 13), ('14', 14), ('15', 15), ('16', 16), ('17', 17), ('18', 18), ('19', 19), ('20', 20), ('21', 21), ('22', 22), ('23', 23)], max_length=2, null=True, unique=True, verbose_name='Godzina')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Cena')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='courts.category', verbose_name='Kategoria')),
            ],
            options={
                'verbose_name': 'cennik',
                'verbose_name_plural': 'Plany cenowe',
            },
        ),
        migrations.AddConstraint(
            model_name='pricelist',
            constraint=models.UniqueConstraint(fields=('category', 'weekend', 'hour'), name='unique_price'),
        ),
    ]
