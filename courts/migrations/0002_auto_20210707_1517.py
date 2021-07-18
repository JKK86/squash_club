# Generated by Django 3.2.4 on 2021-07-07 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data rezerwacji')),
                ('time', models.TimeField(verbose_name='Godzina rezerwacji')),
                ('duration', models.PositiveIntegerField(default=1, verbose_name='Czas rezerwacji')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Cena')),
                ('paid', models.BooleanField(default=False, verbose_name='Opłacone')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Komentarz')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='courts.court', verbose_name='Kort')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name': 'rezerwacja',
                'verbose_name_plural': 'Rezerwacje',
            },
        ),
        migrations.AddConstraint(
            model_name='reservation',
            constraint=models.UniqueConstraint(fields=('court', 'date', 'time'), name='unique_reservation'),
        ),
    ]