# Generated by Django 3.2.4 on 2021-08-11 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courts', '0012_alter_reservation_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Data')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courts.category', verbose_name='Kategoria')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name': 'powiadomienie',
                'verbose_name_plural': 'Powiadomienia',
                'ordering': ['-date'],
            },
        ),
    ]
