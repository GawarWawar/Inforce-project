# Generated by Django 5.0.6 on 2024-07-02 13:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_api', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='day_created',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Day of creation'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='day_of_vote',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Day of vote'),
        ),
    ]
