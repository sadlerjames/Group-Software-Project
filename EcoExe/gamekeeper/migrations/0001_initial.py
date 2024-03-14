# Generated by Django 5.0.1 on 2024-03-12 22:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0003_alter_quizzes_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyQuizzes',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('quiz_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_quiz_id', to='quiz.quizzes')),
            ],
        ),
    ]