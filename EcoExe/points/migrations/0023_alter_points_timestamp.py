# Generated by Django 5.0.2 on 2024-03-14 22:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0022_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 22, 38, 19, 265400, tzinfo=datetime.timezone.utc)),
        ),
    ]
