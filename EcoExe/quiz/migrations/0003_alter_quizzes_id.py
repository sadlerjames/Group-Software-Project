# Generated by Django 5.0.1 on 2024-03-10 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quizzes_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]