# Generated by Django 5.0.3 on 2024-03-19 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quizzes_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='time',
            field=models.IntegerField(),
        ),
    ]
