# Generated by Django 3.1.4 on 2025-01-16 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('cat_pic', models.ImageField(blank=True, null=True, upload_to='photo/')),
            ],
        ),
    ]
