# Generated by Django 3.1.4 on 2025-02-18 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_ordernow'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordernow',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
