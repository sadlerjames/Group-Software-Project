# Generated by Django 5.0.1 on 2024-02-26 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0004_alter_points_timestamp_points_composite_primary_key'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Points',
        ),
    ]
