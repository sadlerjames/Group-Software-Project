# Generated by Django 5.0.1 on 2024-03-13 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0021_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 13, 15, 30, 43, 120587, tzinfo=datetime.timezone.utc)),
        ),
    ]
