# Generated by Django 5.0.3 on 2024-03-20 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0040_remove_dailypoints_composite_primary_key_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailypoints',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 14, 2, 56, 355114, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 14, 2, 56, 355114, tzinfo=datetime.timezone.utc)),
        ),
    ]
