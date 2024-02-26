# Generated by Django 5.0.1 on 2024-02-26 21:55

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0003_rename_points_gained_points_points_and_more'),
        ('quiz', '0002_quizzes_points'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2024, 2, 26, 21, 55, 55, 256580, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddConstraint(
            model_name='points',
            constraint=models.UniqueConstraint(fields=('user_id', 'quiz_id'), name='composite_primary_key'),
        ),
    ]
