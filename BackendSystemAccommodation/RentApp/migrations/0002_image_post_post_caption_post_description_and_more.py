# Generated by Django 5.0.1 on 2024-02-19 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_image', to='RentApp.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='caption',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
