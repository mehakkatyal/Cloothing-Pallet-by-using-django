# Generated by Django 4.2.19 on 2025-02-28 07:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_bag_qu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bag',
            name='date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]
