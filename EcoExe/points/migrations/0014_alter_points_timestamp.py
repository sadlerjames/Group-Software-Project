# Generated by Django 5.0.2 on 2024-03-11 17:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0013_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 11, 17, 35, 44, 314665, tzinfo=datetime.timezone.utc)),
        ),
    ]
