# Generated by Django 5.0.1 on 2024-03-18 10:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0028_alter_dailypoints_timestamp_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailypoints',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 18, 10, 27, 1, 656908, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 18, 10, 27, 1, 656908, tzinfo=datetime.timezone.utc)),
        ),
    ]
