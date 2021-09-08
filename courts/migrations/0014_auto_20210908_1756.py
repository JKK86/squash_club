# Generated by Django 3.2.4 on 2021-09-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0013_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-date', 'created'], 'verbose_name': 'powiadomienie', 'verbose_name_plural': 'Powiadomienia'},
        ),
        migrations.AddField(
            model_name='reservation',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]