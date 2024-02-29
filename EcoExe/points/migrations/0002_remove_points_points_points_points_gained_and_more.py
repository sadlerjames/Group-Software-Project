# Generated by Django 5.0.1 on 2024-02-26 21:54

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0001_initial'),
        ('quiz', '0002_quizzes_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='points',
            name='points',
        ),
        migrations.AddField(
            model_name='points',
            name='points_gained',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='points',
            name='quiz_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quiz_id', to='quiz.quizzes'),
        ),
        migrations.AlterField(
            model_name='points',
            name='timestamp',
            field=models.TimeField(default=datetime.datetime(2024, 2, 26, 21, 54, 2, 96859, tzinfo=datetime.timezone.utc)),
        ),
    ]