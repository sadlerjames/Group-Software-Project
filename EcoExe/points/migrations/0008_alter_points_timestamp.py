# Generated by Django 5.0.1 on 2024-02-27 21:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0007_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2024, 2, 27, 21, 10, 34, 834166, tzinfo=datetime.timezone.utc)),
        ),
    ]