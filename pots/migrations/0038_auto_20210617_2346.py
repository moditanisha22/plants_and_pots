# Generated by Django 3.2 on 2021-06-17 18:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0037_auto_20210616_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_pot',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='pots.address'),
        ),
        migrations.AlterField(
            model_name='order_pot',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 17, 23, 46, 26, 622653)),
        ),
    ]
