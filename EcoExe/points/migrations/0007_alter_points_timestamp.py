# Generated by Django 5.0.1 on 2024-02-26 22:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0006_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2024, 2, 26, 22, 2, 19, 10260, tzinfo=datetime.timezone.utc)),
        ),
    ]
