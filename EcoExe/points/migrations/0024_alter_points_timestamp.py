# Generated by Django 5.0.2 on 2024-03-14 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0023_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 23, 10, 4, 133878, tzinfo=datetime.timezone.utc)),
        ),
    ]
