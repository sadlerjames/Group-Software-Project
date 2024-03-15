# Generated by Django 5.0.2 on 2024-03-15 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('act_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('name', models.TextField()),
                ('info', models.TextField()),
                ('location', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TreasureHunt',
            fields=[
                ('hunt_id', models.AutoField(primary_key=True, serialize=False)),
                ('points', models.IntegerField()),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.TextField(default='/img/Default.png')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('no_points', models.IntegerField()),
                ('information', models.TextField()),
                ('activity_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='treasurehunt.activities')),
                ('hunt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treasurehunt.treasurehunt')),
            ],
            options={
                'unique_together': {('hunt', 'order')},
            },
        ),
        migrations.CreateModel(
            name='UserTreasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.CharField(max_length=100)),
                ('stage_completed', models.BooleanField(default=False)),
                ('no_points', models.IntegerField()),
                ('hunt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treasurehunt.treasurehunt')),
            ],
            options={
                'unique_together': {('hunt', 'player')},
            },
        ),
    ]