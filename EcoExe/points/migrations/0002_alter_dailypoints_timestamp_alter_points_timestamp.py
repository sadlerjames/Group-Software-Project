# Generated by Django 5.0.3 on 2024-03-20 14:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailypoints',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 14, 49, 29, 734732, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 14, 49, 29, 719099, tzinfo=datetime.timezone.utc)),
        ),
    ]