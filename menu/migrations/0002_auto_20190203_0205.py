# Generated by Django 2.1.4 on 2019-02-03 10:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
