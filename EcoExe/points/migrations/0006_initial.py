# Generated by Django 5.0.1 on 2024-02-26 21:58

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('points', '0005_delete_points'),
        ('quiz', '0002_quizzes_points'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('timestamp', models.TimeField(default=datetime.datetime(2024, 2, 26, 21, 58, 36, 773873, tzinfo=datetime.timezone.utc))),
                ('quiz_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quiz_id', to='quiz.quizzes')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='points',
            constraint=models.UniqueConstraint(fields=('user_id', 'quiz_id'), name='composite_primary_key'),
        ),
    ]