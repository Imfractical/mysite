# Generated by Django 2.1.4 on 2019-02-03 10:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20190203_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='created_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]
