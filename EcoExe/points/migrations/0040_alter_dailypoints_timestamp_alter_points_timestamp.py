# Generated by Django 5.0.3 on 2024-03-20 13:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0039_alter_dailypoints_timestamp_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailypoints',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 13, 34, 43, 954238, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 13, 34, 43, 954238, tzinfo=datetime.timezone.utc)),
        ),
    ]
