# Generated by Django 5.0.2 on 2024-03-14 22:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0019_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 22, 9, 2, 549728, tzinfo=datetime.timezone.utc)),
        ),
    ]
