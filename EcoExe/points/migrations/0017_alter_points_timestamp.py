<<<<<<< HEAD
# Generated by Django 5.0.2 on 2024-03-11 18:06
=======
# Generated by Django 5.0.1 on 2024-03-11 20:18
>>>>>>> 9e0d04e7983be82afa3a3b0f71ff81002577ab34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0016_alter_points_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='timestamp',
<<<<<<< HEAD
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 11, 18, 6, 43, 578873, tzinfo=datetime.timezone.utc)),
=======
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 11, 20, 18, 20, 407666, tzinfo=datetime.timezone.utc)),
>>>>>>> 9e0d04e7983be82afa3a3b0f71ff81002577ab34
        ),
    ]
