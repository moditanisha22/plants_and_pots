# Generated by Django 3.2 on 2021-06-03 19:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0003_alter_order_pot_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_pot',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 4, 1, 4, 36, 277793)),
        ),
    ]
