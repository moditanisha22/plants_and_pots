# Generated by Django 3.2 on 2021-06-08 10:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0026_auto_20210608_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_pot',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 8, 16, 15, 20, 815107)),
        ),
    ]
