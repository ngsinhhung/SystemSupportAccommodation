# Generated by Django 5.0.1 on 2024-01-30 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostpost',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
